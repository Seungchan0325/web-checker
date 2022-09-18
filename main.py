from web_info import *
import argparse
import re
import requests
from urllib.parse import urlparse, urlunparse, ParseResult

def is_valid_url(url: str) -> bool:
    try:
        res = requests.get(url)
    except:
        return False
    return res.status_code == 200

def get_port(url: ParseResult) -> int:
    if url.scheme == 'http':
        return 80
    elif url.scheme == 'https':
        return 443

def main(args):
    url = urlparse(args.url)
    
    if not is_valid_url(args.url):
        raise ValueError(f"Invalid URL: {args.url}\nPlease check URL or Check server is opened")
    
    if url.port is None:
        url = url._replace(netloc=url.netloc+':'+str(get_port(url)))
    
    web = web_info(url.hostname, url.port)
    weights = [100]
    verifications = []

    verifications.append(web.verify_ssl())
    
    #I used weighted sum
    #reliability = verifications[0] * weights[0] + verifications[1] * weights[1] + ...
    reliability = 0
    for verification, weight in zip(verifications, weights):
        reliability = reliability + weight * verification

    print(f'reliability is {sum(weights) * 100 / reliability}%')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', required=True, 
        help="url to check into (example 'http(s)://example.com')")
    
    try:
        main(parser.parse_args())
    except Exception as e:
        print(e, end='\n\n')
        parser.print_help()
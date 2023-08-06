import sys
import argparse
import datetime
import re
import os
import base64
import random
from datetime import datetime
from list_uas import ua_list


parser = argparse.ArgumentParser(description='Tool suite')
parser.add_argument('-b', '--base64', required=False,
        help='Base64 decoding; prompts for string', nargs='*')
parser.add_argument('-u', '--useragent', required=False,
        help='Generate a random UA string', nargs='*')
args = vars(parser.parse_args())

def b64_function():
    b64_d_string = input('Input string to decode:')
    output = base64.b64decode(b64_d_string)
    print(output)
    exit

def user_agents():
    ua = random.choice(ua_list)
    print(ua)
    exit


def main():
    if args['base64'] is not None:
        b64_function()
    if args['useragent'] is not None:
        user_agents()
if __name__ == '__main__':
    main()

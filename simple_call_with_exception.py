#!/usr/bin/env python3
import os
import argparse
from time import time
from pprint import pprint

import asyncio

from Bitlish import Bitlish, BitlishError

TOKEN = os.getenv('TOKEN')
TOKEN = TOKEN or "fixed:qweqwe"

parser = argparse.ArgumentParser(description='Simple call with exception handling')
parser.add_argument('-t', '--token', help='API token')


@asyncio.coroutine
def main():
    api = yield from Bitlish(TOKEN, timeout=10, throw_errors=True).init()

    try:
        resp = yield from api.list_tokens({
            'page': '[]',  # invalid number
        })
    except BitlishError as e:
        print('API Error: ', e)
    else:
        tokens = resp["data"]
        print('\nTokens:')
        pprint(tokens)

    api.stop()


if __name__ == '__main__':
    args = parser.parse_args()
    TOKEN = args.token or TOKEN

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()

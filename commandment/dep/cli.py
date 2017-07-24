import argparse
import logging
import asyncio
from commandment.dep.dep import DEP

parser = argparse.ArgumentParser()
parser.add_argument("consumer_key", help="The decrypted consumer_key from the DEP stoken")
parser.add_argument("consumer_secret", help="The decrypted consumer_secret from the DEP stoken")
parser.add_argument("access_token", help="The decrypted access_token from the DEP stoken")
parser.add_argument("access_secret", help="The decrypted access_secret from the DEP stoken")
parser.add_argument("--url", help="The URL of the DEP Service", default="https://mdmenrollment.apple.com")

logger = logging.getLogger(__name__)
logging.getLogger('asyncio').setLevel(logging.WARNING)

async def initial_dep_fetch(dep: DEP):
    """Perform the initial DEP fetch, if required."""
    for page in dep.devices():
        for device in page:
            pass

async def dep_sync(consumer_key: str, consumer_secret: str, access_token: str, access_secret: str, url: str):
    dep = DEP(consumer_key, consumer_secret, access_token, access_secret, url)
    initial_fetch = await initial_dep_fetch(dep)


def main():
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()

    loop.run_until_complete(dep_sync(
        args.consumer_key,
        args.consumer_secret,
        args.access_token,
        args.access_secret,
        args.url,
    ))

    try:
        loop.run_forever()
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()
    

if __name__ == "__main__":
    main()

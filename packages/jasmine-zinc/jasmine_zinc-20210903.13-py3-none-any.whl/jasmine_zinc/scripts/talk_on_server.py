import os
from jasmine_zinc import (
    talk_on_server,
    Talk,
    add_talk_arguments,
)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-cid', '--cid', type=int, required=True)
    parser.add_argument('-t', '--talktext', type=str)
    parser.add_argument('-f', '--talkfile', type=str)
    parser.add_argument('--server-url', type=str, default=os.environ.get('SERVER_URL'), help='AssistantSeika HTTP Server')
    parser.add_argument('--connect-timeout', type=float, default=3)
    parser.add_argument('--read-timeout', type=float, default=None)
    add_talk_arguments(parser=parser)
    args = parser.parse_args()

    server_url = args.server_url
    timeout = (args.connect_timeout, args.read_timeout)

    assert server_url is not None, 'Server URL must be specified (option --server-url or env var SERVER_URL).'

    cid = args.cid
    talktext = args.talktext
    talkfile = args.talkfile

    assert (talktext is not None) ^ (talkfile is not None), 'One of --talktext or --talkfile is required.'

    if talkfile:
        with open(talkfile, 'r') as fp:
            talktext = fp.read()

    result = talk_on_server(
        server_url=server_url,
        cid=cid,
        talk=Talk(
            talktext=talktext,
        ),
        timeout=timeout,
    )

    print(result)

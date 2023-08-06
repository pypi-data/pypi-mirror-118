import os
from jasmine_zinc import get_avatars

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--server-url', type=str, default=os.environ.get('SERVER_URL'), help='AssistantSeika HTTP Server')
    parser.add_argument('--timeout', type=float, default=3)
    args = parser.parse_args()

    server_url = args.server_url
    assert server_url is not None, 'Server URL must be specified (option --server-url or env var SERVER_URL).'

    timeout = args.timeout

    avatars = get_avatars(
        server_url=server_url,
        timeout=timeout,
    )

    print(avatars)

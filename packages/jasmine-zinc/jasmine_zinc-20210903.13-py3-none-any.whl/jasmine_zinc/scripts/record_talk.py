import os
from jasmine_zinc import (
    record_talk,
    Talk,
    add_talk_arguments,
)
from playsound import playsound
import tempfile
from shutil import copyfile

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-cid', '--cid', type=int, required=True)
    parser.add_argument('-t', '--talktext', type=str)
    parser.add_argument('-f', '--talkfile', type=str)
    parser.add_argument('--frequency', type=int, default=48000)
    parser.add_argument('--no-play', action='store_true')
    parser.add_argument('--save', action='store_true')
    parser.add_argument('--save-path', type=str, default='output.wav')
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

    frequency = args.frequency

    no_play = args.no_play
    save = args.save
    save_path = args.save_path

    result = record_talk(
        server_url=server_url,
        cid=cid,
        talk=Talk(
            talktext=talktext,
        ),
        frequency=frequency,
        timeout=timeout,
    )

    with tempfile.NamedTemporaryFile() as fp:
        fp.write(result.wave_binary)
        fp.seek(0)

        if not no_play:
            playsound(fp.name)

        if save:
            copyfile(fp.name, save_path)

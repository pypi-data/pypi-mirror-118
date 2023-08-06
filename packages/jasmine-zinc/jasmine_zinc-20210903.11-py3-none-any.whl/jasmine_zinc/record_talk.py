from urllib.parse import urljoin
import json
import requests
from dataclasses import dataclass

from .Talk import (
    Talk,
    talk2dict,
)

FREQUENCIES = [
    8000,
    16000,
    22050,
    44100,
    48000,
]

@dataclass
class RecordTalkResponse:
    wave_binary: bytes

def record_talk(
    server_url: str,
    cid: int,
    talk: Talk,
    frequency: int,
    timeout: float = 3,
) -> RecordTalkResponse:
    api_url = urljoin(server_url, f'SAVE2/{int(cid)}/{int(frequency)}')

    headers = {
        'Content-Type': 'application/json',
    }

    data = talk2dict(talk=talk)

    r = requests.post(api_url, headers=headers, data=json.dumps(data), timeout=timeout)

    response = r.content

    ret = RecordTalkResponse(
        wave_binary=response,
    )

    return ret

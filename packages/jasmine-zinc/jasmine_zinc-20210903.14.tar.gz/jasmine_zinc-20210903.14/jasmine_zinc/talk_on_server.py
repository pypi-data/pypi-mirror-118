from urllib.parse import urljoin
import json
import requests
from dataclasses import dataclass
from typing import Union, Tuple, Optional

from .Talk import (
    Talk,
    talk2dict,
)

@dataclass
class TalkOnServerResponse:
    message: str

def talk_on_server(
    server_url: str,
    cid: int,
    talk: Talk,
    timeout: Union[Optional[float], Tuple[Optional[float], Optional[float]]] = (3, None),
) -> TalkOnServerResponse:
    api_url = urljoin(server_url, f'PLAY2/{int(cid)}')

    headers = {
        'Content-Type': 'application/json',
    }

    data = talk2dict(talk=talk)

    r = requests.post(api_url, headers=headers, data=json.dumps(data), timeout=timeout)

    response = r.json()

    ret = TalkOnServerResponse(
        message=response['message'],
    )

    return ret

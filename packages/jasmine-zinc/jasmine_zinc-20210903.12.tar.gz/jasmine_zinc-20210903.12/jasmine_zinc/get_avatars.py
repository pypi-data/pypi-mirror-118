from urllib.parse import urljoin
import requests
from typing import Dict, List, Any

from .Avatar import (
    Avatar,
    dict2avatar,
)

def get_avatars(
    server_url: str,
    timeout: float = 3,
) -> Dict[str, Any]:
    api_url = urljoin(server_url, 'AVATOR2')
    r = requests.get(api_url, timeout=timeout)

    avatar_list = r.json()
    avatars: List[Avatar] = []

    for avatar in avatar_list:
        avatars.append(dict2avatar(dic=avatar))

    return avatars

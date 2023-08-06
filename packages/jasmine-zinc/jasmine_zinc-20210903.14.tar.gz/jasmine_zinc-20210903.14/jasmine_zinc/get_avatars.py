from urllib.parse import urljoin
import requests
from typing import Dict, List, Any, Union, Tuple

from .Avatar import (
    Avatar,
    dict2avatar,
)

def get_avatars(
    server_url: str,
    timeout: Union[float, Tuple[float, float]] = None,
) -> List[Avatar]:
    api_url = urljoin(server_url, 'AVATOR2')
    r = requests.get(api_url, timeout=timeout)

    avatar_list = r.json()
    avatars: List[Avatar] = []

    for avatar in avatar_list:
        avatars.append(dict2avatar(dic=avatar))

    return avatars

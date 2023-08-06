from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class Avatar:
    cid: int
    name: str
    platform: str
    prod: str

def dict2avatar(dic: Dict[str, Any]) -> Avatar:
    return Avatar(
        cid=dic['cid'],
        name=dic['name'],
        platform=dic['platform'],
        prod=dic['prod'],
    )

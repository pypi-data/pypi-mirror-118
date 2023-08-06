#!/usr/bin/env python3

import time
import requests
from json import dumps
from typing import Any, Dict, List, Optional, Union


def jsonPrint(
    content: Optional[Union[Dict[str, Any], List[Any]]] = {},
    title: Optional[str] = None,
) -> None:
    if title is not None:
        data = {title: content}
    else:
        data = content
    print(dumps(data, indent=2))

class Fetch:
    def __init__(self, url: str):
        self.base_url = url

    def __call__(self, endpoint: str) -> Optional[str]:
        url = self.base_url + endpoint
        print("\rFetching URL:", url, end="")
        response = requests.get(url, timeout=4)
        if not response.ok:
            print("Waiting for response...", end="")
            while not response.ok:
                response = requests.get(url, timeout=4)
                time.sleep(1)
        print(" [OK]")
        return response.text or None
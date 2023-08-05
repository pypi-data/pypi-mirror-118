#!/usr/bin/env python3

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

#!/usr/bin/env python3

from typing import Optional


class CFBase:
    def __init__(self) -> None:
        self.base_url = "https://api.cloudflare.com/client/v4"

    def build_url(self, path: Optional[str] = None) -> str:
        base_path = "" if not hasattr(self, "base_path") else self.base_path
        if path is None:
            return f"{self.base_url}{base_path}"
        if path.startswith("/"):
            return f"{self.base_url}{base_path}{path}"
        return f"{self.base_url}{base_path}/{path}"

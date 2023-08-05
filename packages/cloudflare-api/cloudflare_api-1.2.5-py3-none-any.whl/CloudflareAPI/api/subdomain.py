#!/usr/bin/env python3

from re import match
from typing import Any, Dict, Optional
from CloudflareAPI.base import CFBase
from CloudflareAPI.exceptions import CFError
from CloudflareAPI.network import Request


class Subdomain(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/workers/subdomain"
        super().__init__()

    def create(self, name: str) -> str:
        name = name.replace("_", "-").lower()
        if not match("^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$", name):
            raise CFError("Subdomain is not valid")
        url = self.build_url()
        return self.req.put(url, json=dict(subdomain=name))

    def get(self) -> str:
        url = self.build_url()
        return self.req.get(url)["subdomain"]

#!/usr/bin/env python3

from CloudflareAPI.core import CFBase, Request


class User(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/user"
        super().__init__()

    def details(self, minimal: bool = True):
        url = self.build_url()
        data = self.req.get(url)
        if minimal and "organizations" in data.keys():
            del data["organizations"]
        return data

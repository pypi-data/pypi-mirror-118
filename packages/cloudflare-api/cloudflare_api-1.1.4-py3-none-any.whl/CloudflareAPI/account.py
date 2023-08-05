#!/usr/bin/env python3

from CloudflareAPI.base import CFBase
from CloudflareAPI.network import Request
from CloudflareAPI.exceptions import CFError


class Account(CFBase):
    def __init__(self, request: Request) -> None:
        self.req = request
        self.base_path = "/accounts"
        super().__init__()

    def list(self):
        url = self.build_url()
        accounts = self.req.get(url)
        return accounts

    def get_id(self) -> str:
        alist = self.list()
        if len(alist) == 1:
            return alist[0]["id"]
        if len(alist) > 1:
            print("Please use one of the account id as parameter in Cloudflare class")
            print("Accounts: ")
            for account in self.list():
                print("   ", account["name"], ":", account["id"])
            exit()
        raise CFError("No account found")

    def details(self, aid: str):
        url = self.build_url(aid)
        account = self.req.get(url)
        return account

    def rename(self, aid: str, name: str):
        url = self.build_url(aid)
        account = self.req.put(url, json=dict(name=name))
        return account

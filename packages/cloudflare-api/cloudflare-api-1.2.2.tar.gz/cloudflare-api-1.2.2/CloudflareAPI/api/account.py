#!/usr/bin/env python3

from typing import Any, Dict, Optional
from CloudflareAPI.base import CFBase
from CloudflareAPI.network import Request
from CloudflareAPI.exceptions import CFError


class Account(CFBase):
    def __init__(self, request: Request) -> None:
        self.req = request
        self.base_path = "/accounts"
        super().__init__()

    def list(
        self, detailed: bool = False, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        url = self.build_url()
        accounts = self.req.get(url)
        if not detailed:
            accounts = {account["name"]: account["id"] for account in accounts}
        return accounts

    def get_id(self) -> str:
        alist = self.list(detailed=True)
        if len(alist) == 1:
            return alist[0]["id"]
        if len(alist) > 1:
            print("Please use one of the account id as parameter in Cloudflare class")
            print("Accounts: ")
            for account in self.list():
                print("   ", account["name"], ":", account["id"])
            exit()
        raise CFError("No account found")

    def details(self, account_id: str):
        url = self.build_url(account_id)
        account = self.req.get(url)
        return account

    # This method is not accessable due to default token permissions
    def rename(self, account_id: str, name: str):
        url = self.build_url(account_id)
        account = self.req.put(url, json=dict(name=name))
        return account

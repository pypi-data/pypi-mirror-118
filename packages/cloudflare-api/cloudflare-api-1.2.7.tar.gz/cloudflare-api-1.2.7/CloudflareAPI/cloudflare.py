#!/usr/bin/env python3

from typing import Optional
from CloudflareAPI.core import CFBase, Request
from CloudflareAPI.api import Account, Worker, Storage, User


class Cloudflare(CFBase):
    def __init__(self, token: str, account_id: Optional[str] = None) -> None:
        self.__token = token
        self.account_id = account_id
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.req = Request(base=self.base_url, token=self.__token)
        self.account = Account(request=self.req)
        if not self.account_id or self.account_id is None:
            self.account_id = self.account.get_id()
        self.user = User(request=self.req, account_id=self.account_id)
        self.worker = Worker(request=self.req, account_id=self.account_id)
        self.store = Storage(request=self.req, account_id=self.account_id)

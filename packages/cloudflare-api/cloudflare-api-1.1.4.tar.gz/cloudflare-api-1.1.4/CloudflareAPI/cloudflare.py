#!/usr/bin/env python3

from typing import Optional
from CloudflareAPI.base import CFBase
from CloudflareAPI.network import Request
from CloudflareAPI.workers import Worker
from CloudflareAPI.storage import Storage
from CloudflareAPI.account import Account


class Cloudflare(CFBase):
    def __init__(self, token: str, account_id: Optional[str] = None) -> None:
        self.__token = token
        self.__id = account_id
        self.base_url = "https://api.cloudflare.com/client/v4"
        self.req = Request(base=self.base_url, token=self.__token)
        self.account = Account(request=self.req)
        if not self.__id or self.__id is None:
            self.__id = self.account.get_id()
        self.worker = Worker(request=self.req, account_id=self.__id)
        self.store = Storage(request=self.req, account_id=self.__id)

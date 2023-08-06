#!/usr/bin/env python3


from typing import Any, Dict, List
from CloudflareAPI.core import CFBase, Request


class Cron(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/workers/scripts"
        super().__init__()

    def update(self, worker: str, crons: List[str]) -> Any:
        url = self.build_url(f"/{worker}/schedules")
        crons = [{"cron": cron} for cron in crons]
        return self.req.put(url, json=crons)["schedules"]

    def get(self, worker: str) -> Any:
        url = self.build_url(f"/{worker}/schedules")
        return self.req.get(url)["schedules"]

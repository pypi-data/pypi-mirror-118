#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from CloudflareAPI.base import CFBase
from CloudflareAPI.network import Request


class Worker(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/workers/scripts"
        super().__init__()

    def list(
        self, detailed: bool = False, params: Optional[Dict[str, Any]] = None
    ) -> List:
        url = self.build_url()
        workers = self.req.get(url, params=params)
        if detailed:
            wlist = [
                {
                    worker["id"]: [
                        {item["script"]: item["pattern"]} for item in worker["routes"]
                    ]
                }
                if worker["routes"] is not None
                else {worker["id"]: "No routes"}
                for worker in workers
            ]
        else:
            wlist = [worker["id"] for worker in workers]
        return wlist

    def download(self, name: str, directory: str = "./workers") -> int:
        url = self.build_url(name)
        data = self.req.get(url)
        directory = Path(directory)
        directory.mkdir(parents=True, exist_ok=True)
        directory.resolve(strict=True)
        file = directory / f"{name}.js"
        return file.write_text(data)

    def upload(
        self,
        name: str,
        file: str,
        bindings: Optional[Union[List[Dict[str, str]], Dict[str, str]]] = None,
    ) -> None:
        file = Path(file)
        file.resolve(strict=True)
        url = self.build_url(name)
        if bindings is None:
            data = file.read_text()
            return self.cf.put(url, data=data)
        if not isinstance(bindings, list):
            bindings = [bindings]
        metadata = {
            "body_part": "script",
            "bindings": [
                {
                    "name": binding["name"].upper(),
                    "type": "kv_namespace",
                    "namespace_id": binding["id"],
                }
                for binding in bindings
            ],
        }
        miltipart_data = {
            "metadata": (None, json.dumps(metadata), "application/json"),
            "script": (
                file.name,
                file.open("rb"),
                "application/javascript",
            ),
        }
        return self.req.put(url, files=miltipart_data)

    def delete(self, name: str) -> None:
        url = self.build_url(name)
        return self.req.delete(url)

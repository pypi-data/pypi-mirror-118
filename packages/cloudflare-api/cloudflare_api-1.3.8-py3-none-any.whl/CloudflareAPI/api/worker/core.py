#!/usr/bin/env python3

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from CloudflareAPI.core import CFBase, Request
from CloudflareAPI.api.worker.cron import Cron
from CloudflareAPI.api.worker.subdomain import Subdomain


class Worker(CFBase):
    class Metadata:
        def __init__(self) -> None:
            self.data = dict(body_part="script", bindings=[])

        def __call__(self):
            return (None, json.dumps(self.data), "application/json")

        def _sanitize(self, text: str):
            return text.strip().replace(" ","_").upper()

        def add_binding(self, name: str, namespace_id: str):
            binding = dict(
                name=self._sanitize(name), type="kv_namespace", namespace_id=namespace_id
            )
            self.data["bindings"].append(binding)

        def add_variable(self, name: str, text: str):
            binding = dict(name=self._sanitize(name), type="plain_text", text=text)
            self.data["bindings"].append(binding)

        def add_secret(self, name: str, secret: str):
            binding = dict(name=self._sanitize(name), type="secret_text", text=secret)
            self.data["bindings"].append(binding)
        

    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/workers/scripts"
        self.cron = Cron(request, account_id)
        self.subdomain = Subdomain(request, account_id)
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
        metadata: Optional[Metadata] = None
    ) -> Any:
        file = Path(file)
        file.resolve(strict=True)
        url = self.build_url(name)
        if metadata is None:
            data = file.read_text()
            return self.req.put(url, data=data, headers={"Content-Type": "application/javascript"})
        miltipart_data = {
            "metadata": metadata(),
            "script": (
                file.name,
                file.open("rb"),
                "application/javascript",
            ),
        }
        return self.req.put(url, files=miltipart_data)

    def deploy(self, name: str) -> bool:
        url = self.build_url(f"{name}/subdomain")
        return self.req.post(url, json={"enabled": True})

    def undeploy(self, name: str) -> bool:
        url = self.build_url(f"{name}/subdomain")
        return self.req.post(url, json={"enabled": False})

    def delete(self, name: str) -> bool:
        url = self.build_url(name)
        return self.req.delete(url)

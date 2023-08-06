#!/usr/bin/env python3

from typing import Any, Dict, Optional
from CloudflareAPI.core import CFBase, Request
from CloudflareAPI.exceptions import CFError


class Storage(CFBase):
    def __init__(self, request: Request, account_id: str) -> None:
        self.req = request
        self.base_path = f"/accounts/{account_id}/storage/kv/namespaces"
        super().__init__()

    def list(
        self, detailed: bool = False, params: Optional[Dict[str, Any]] = None
    ) -> Any:
        url = self.build_url()
        nslist: Any = self.req.get(url, params=params)
        if not detailed:
            nslist = {ns["title"]: ns["id"] for ns in nslist}
        return nslist

    def get_id(self, namespace: str):
        stores = self.list()
        namespace = namespace.upper()
        if namespace in stores:
            return stores[namespace]
        raise CFError("Namespace not found")

    def create(self, namespace: str) -> bool:
        namespace = namespace.upper()
        url = self.build_url()
        result = self.req.post(url, json=dict(title=namespace))
        if result["title"] == namespace:
            return result["id"]
        raise CFError("Unable to create namespace")

    def rename(self, old_namespace: str, new_namespace: str):
        old_namespace = old_namespace.upper()
        new_namespace = new_namespace.upper()
        store_id = self.get_id(old_namespace)
        url = self.build_url(store_id)
        return self.req.put(url, json={"title": new_namespace})

    def delete(self, namespace: str):
        namespace = namespace.upper()
        store_id = self.get_id(namespace)
        url = self.build_url(store_id)
        return self.req.delete(url)

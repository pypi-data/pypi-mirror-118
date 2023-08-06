#!/usr/bin/env python3


class CFError(Exception):
    ...


class APIError(CFError):
    def __init__(self, errors, *args, **kargs) -> None:
        if len(errors) > 0:
            self.code = errors[0]["code"]
            self.message = errors[0]["message"]
            super().__init__(self.message, *args, **kargs)
        else:
            raise CFError("Unknown internal error")

    def __str__(self) -> str:
        return f"{self.code}: {self.message}"

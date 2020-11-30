from typing import Any

class Messages:
    def create(self, to: str, from_: str, body: str) -> Any: ...

class Client:
    messages: Messages

class rest:
    @staticmethod
    def Client() -> Client: ...

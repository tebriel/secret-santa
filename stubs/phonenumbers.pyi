from typing import Any, Optional


def parse(number: str, region: Optional[str]) -> Any: ...
def format_number(number: Any, format: Any) -> str: ...

class PhoneNumberFormat:
    E164: str

from dataclasses import dataclass
from typing import Optional


@dataclass
class ResponseContainer[T]:
    status_code: int
    headers: dict
    content: Optional[T] | Optional[str] = None

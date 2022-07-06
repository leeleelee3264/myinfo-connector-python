from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True)
class MyinfoAuthoriseRedirectUrl:
    state: UUID
    url: str

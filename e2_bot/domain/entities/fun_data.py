from dataclasses import dataclass


@dataclass
class FunData:
    content_type: str
    file_id: str
    answer: str



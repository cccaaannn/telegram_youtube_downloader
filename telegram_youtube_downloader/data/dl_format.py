from dataclasses import dataclass


@dataclass
class DlFormat:
    name: str
    value: str
    is_default: bool = False

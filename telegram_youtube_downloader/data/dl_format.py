from dataclasses import dataclass


@dataclass
class DlFormat:
    name: str
    value: str
    is_default: bool

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data.get("name", ""),
            value=data.get("value", ""),
            is_default=data.get("is_default", False)
        )

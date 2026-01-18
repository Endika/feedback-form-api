from dataclasses import dataclass


@dataclass(frozen=True)
class ResponseId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not isinstance(self.value, str):
            msg = "ResponseId must be a non-empty string"
            raise ValueError(msg)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ResponseId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

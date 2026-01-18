from dataclasses import dataclass


@dataclass(frozen=True)
class QuestionId:
    value: str

    def __post_init__(self) -> None:
        if not self.value or not isinstance(self.value, str):
            msg = "QuestionId must be a non-empty string"
            raise ValueError(msg)

    def __str__(self) -> str:
        return self.value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, QuestionId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

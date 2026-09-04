from dataclasses import dataclass


@dataclass(frozen=True)
class Train:
    train_no: int
    host: str
    username: str

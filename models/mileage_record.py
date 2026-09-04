from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class MileageRecord:
    train_no: int
    timestamp: Optional[str]
    meters: Optional[int]
    decimeters: Optional[int]
    mileage_km: Optional[float]
    speed_kmh: Optional[int]
    status: str
    error: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)

import re
from models.mileage_record import MileageRecord


class MileageParser:
    _pattern = re.compile(
        r"^(?P<timestamp>\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2}\.\d{3}).*?"
        r"VCU odometry update w/ meters (?P<meters>\d+), "
        r"decimeters (?P<decimeters>\d+) and speed (?P<speed>-?\d+) km/h"
    )

    def parse_latest(self, train_no: int, log_text: str) -> MileageRecord:
        # Search backwards so the first match is the latest odometry record.
        for line in reversed(log_text.splitlines()):
            match = self._pattern.search(line)
            if not match:
                continue

            meters = int(match.group("meters"))
            decimeters = int(match.group("decimeters"))
            speed = int(match.group("speed"))
            mileage_km = (meters + decimeters / 10.0) / 1000.0

            return MileageRecord(
                train_no=train_no,
                timestamp=match.group("timestamp"),
                meters=meters,
                decimeters=decimeters,
                mileage_km=mileage_km,
                speed_kmh=speed,
                status="ok",
            )

        return MileageRecord(
            train_no=train_no,
            timestamp=None,
            meters=None,
            decimeters=None,
            mileage_km=None,
            speed_kmh=None,
            status="no_data",
            error="LOG 尾端找不到 VCU odometry update",
        )

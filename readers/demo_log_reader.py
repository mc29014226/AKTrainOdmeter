from datetime import datetime

from models.train import Train
from readers.base_log_reader import BaseLogReader


class DemoLogReader(BaseLogReader):
    """Generate AVL-compatible sample records for Codespaces/UI testing."""

    def read_tail(self, train: Train, remote_path: str, line_count: int = 800) -> str:
        del remote_path, line_count

        # Deterministic fake values so every train has a different row in demo mode.
        meters = 141_000_000 + (train.train_no - 200) * 100_000
        decimeters = train.train_no % 10
        speed = (train.train_no * 3) % 26
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        return (
            f"{timestamp} INFO  [avlmanager.cpp      :462 ] "
            f"VCU odometry update w/ meters {meters}, "
            f"decimeters {decimeters} and speed {speed} km/h\n"
        )

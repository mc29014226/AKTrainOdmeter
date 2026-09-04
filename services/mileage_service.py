from concurrent.futures import ThreadPoolExecutor, as_completed

from models.mileage_record import MileageRecord
from models.train import Train
from parsers.mileage_parser import MileageParser
from readers.base_log_reader import BaseLogReader


class MileageService:
    def __init__(
        self,
        trains: list[Train],
        reader: BaseLogReader,
        parser: MileageParser,
        remote_log_path: str,
        tail_lines: int = 800,
        max_workers: int = 5,
    ):
        self._trains = trains
        self._reader = reader
        self._parser = parser
        self._remote_log_path = remote_log_path
        self._tail_lines = tail_lines
        self._max_workers = max_workers

    def _read_one(self, train: Train) -> MileageRecord:
        try:
            text = self._reader.read_tail(
                train=train,
                remote_path=self._remote_log_path,
                line_count=self._tail_lines,
            )
            return self._parser.parse_latest(train.train_no, text)
        except Exception as exc:
            return MileageRecord(
                train_no=train.train_no,
                timestamp=None,
                meters=None,
                decimeters=None,
                mileage_km=None,
                speed_kmh=None,
                status="error",
                error=str(exc),
            )

    def get_all_mileage(self) -> list[dict]:
        results: list[MileageRecord] = []

        with ThreadPoolExecutor(max_workers=self._max_workers) as pool:
            future_map = {pool.submit(self._read_one, train): train for train in self._trains}
            for future in as_completed(future_map):
                results.append(future.result())

        results.sort(key=lambda item: item.train_no)
        return [item.to_dict() for item in results]

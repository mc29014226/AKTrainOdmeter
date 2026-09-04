from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

import config
from models.train import Train
from parsers.mileage_parser import MileageParser
from readers.demo_log_reader import DemoLogReader
from services.mileage_service import MileageService

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Train Mileage Reader", version="0.2.0")

trains = [
    Train(train_no=no, host=host, username=config.SSH_USERNAME)
    for no, host in config.TRAIN_HOSTS.items()
]

if config.APP_MODE == "demo":
    reader = DemoLogReader()
else:
    from readers.ssh_log_reader import SshLogReader

    reader = SshLogReader(
        password=config.SSH_PASSWORD,
        port=config.SSH_PORT,
        timeout=config.SSH_TIMEOUT_SECONDS,
    )

service = MileageService(
    trains=trains,
    reader=reader,
    parser=MileageParser(),
    remote_log_path=config.REMOTE_LOG_PATH,
    tail_lines=config.TAIL_LINES,
    max_workers=config.MAX_WORKERS,
)


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "web" / "index.html")


@app.post("/api/mileage")
def read_all_mileage():
    return {
        "mode": config.APP_MODE,
        "count": len(trains),
        "results": service.get_all_mileage(),
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "mode": config.APP_MODE}

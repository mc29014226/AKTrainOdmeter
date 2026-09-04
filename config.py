import os

from dotenv import load_dotenv

load_dotenv()

APP_MODE = os.getenv("APP_MODE", "ssh").strip().lower()
REMOTE_LOG_PATH = "/opt/log/04_obcur2_app/avl.log"
SSH_PORT = 22
SSH_USERNAME = os.getenv("SSH_USERNAME", "thalesadmin")
SSH_PASSWORD = os.getenv("SSH_PASSWORD", "")
SSH_TIMEOUT_SECONDS = 6
TAIL_LINES = 800
MAX_WORKERS = 5

TRAIN_HOSTS = {
    201: "192.168.97.1",
    202: "192.168.98.1",
    203: "192.168.99.1",
    204: "192.168.100.1",
    205: "192.168.101.1",
    206: "192.168.102.1",
    207: "192.168.103.1",
    208: "192.168.104.1",
    209: "192.168.105.1",
    210: "192.168.106.1",
    211: "192.168.107.1",
    212: "192.168.108.1",
    213: "192.168.109.1",
    214: "192.168.110.1",
    215: "192.168.111.1",
}

import shlex

import paramiko

from models.train import Train
from readers.base_log_reader import BaseLogReader


class SshLogReader(BaseLogReader):
    def __init__(self, password: str, port: int = 22, timeout: int = 6):
        self._password = password
        self._port = port
        self._timeout = timeout

    def read_tail(self, train: Train, remote_path: str, line_count: int = 800) -> str:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            client.connect(
                hostname=train.host,
                port=self._port,
                username=train.username,
                password=self._password,
                timeout=self._timeout,
                banner_timeout=self._timeout,
                auth_timeout=self._timeout,
                look_for_keys=False,
                allow_agent=False,
            )

            command = f"tail -n {int(line_count)} {shlex.quote(remote_path)}"
            _, stdout, stderr = client.exec_command(command, timeout=self._timeout)
            output = stdout.read().decode("utf-8", errors="replace")
            error = stderr.read().decode("utf-8", errors="replace").strip()
            exit_status = stdout.channel.recv_exit_status()

            if exit_status != 0:
                raise RuntimeError(error or f"tail command failed, exit={exit_status}")

            return output
        finally:
            client.close()

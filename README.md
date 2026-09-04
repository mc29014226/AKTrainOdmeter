# Train Mileage Reader

第一版列車里程讀取工具：按下網頁上的「讀取全部里程」，解析最新一筆 VCU odometry 並顯示 201～215 車里程。

## GitHub Codespaces

本專案已包含 `.devcontainer/devcontainer.json`。建立 Codespace 後會自動安裝 Python 套件，且預設使用 `APP_MODE=demo`，因此即使 Codespace 無法連公司 `192.168.x.x` 內網，也能先測試 HTML、API 與 Parser。

在 Codespace Terminal 執行：

```bash
./run.sh
```

Port 8000 會自動轉發，開啟預覽後按「讀取全部里程」。畫面顯示 `DEMO 模式（Codespaces 測試資料）` 代表目前不是讀真車。

## 公司內網真車模式

真車資料來源：

```text
/opt/log/04_obcur2_app/avl.log
```

在能連到列車 OBCU 的公司內網電腦設定 `.env`：

```text
APP_MODE=ssh
SSH_USERNAME=thalesadmin
SSH_PASSWORD=你的密碼
```

然後執行：

```bash
pip install -r requirements.txt
./run.sh
```

> GitHub Codespaces 是雲端環境；除非另有公司允許的 VPN/網路通道，否則通常無法直接連到 192.168.x.x 私有網段。因此 Codespaces 用於開發與測試，真車讀取需在可達 OBCU 的執行環境使用 `APP_MODE=ssh`。

## OOP 結構

```text
models/                  Train / MileageRecord
readers/base_log_reader  Reader 抽象介面
readers/demo_log_reader  Codespaces 測試資料
readers/ssh_log_reader   真車 SSH 讀取 LOG 尾端
parsers/                 解析 VCU odometry
services/                串接各車讀取流程
web/index.html           HTML 操作介面
main.py                  FastAPI 入口
config.py                IP / LOG 路徑 / 執行模式
```

## 測試

```bash
pytest
```

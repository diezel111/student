import subprocess
import sys
import time
from datetime import datetime

# === Автоустановка requests, если не установлен ===
try:
    import requests
except ImportError:
    print("Модуль 'requests' не найден. Устанавливаю...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests"])
    import requests

# === Настройки ===
BYBIT_URL = "https://api.bybit.com/v5/market/instruments-info"
PARAMS = {
    "category": "linear",
    "status": "PreLaunch",
    "limit": 800
}
LOG_FILE = r"C:\Users\user2\Documents\GitHub\student\bybit\prelaunch_log.txt"

def log_to_file(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")

def check_prelaunch():
    try:
        r = requests.get(BYBIT_URL, params=PARAMS, timeout=10)
        data = r.json()
        if data["retCode"] != 0:
            log_to_file(f"API ошибка: {data['retMsg']}")
            return

        symbols = data["result"].get("list", [])
        if not symbols:
            log_to_file("Прелистингов нет.")
            return

        log_to_file("🔥 Обнаружены PreLaunch инструменты:")
        for s in symbols:
            line = f"{s['symbol']} ({s.get('baseCoin', '')})"
            log_to_file("    " + line)

    except Exception as e:
        log_to_file(f"Ошибка запроса: {e}")

if __name__ == "__main__":
    log_to_file("=== Запуск мониторинга PreLaunch на Bybit ===")
    while True:
        check_prelaunch()
        time.sleep(300)  # проверка каждые 5 минут

import socket
import time
import os
from pathlib import Path
from datetime import datetime
from src.modules.proxy_config_writer import update_config, load_proxies, save_proxies
from src.modules.notifier import notify_admin

# Константи
LOG_DIR = "logs"
LOG_FILE = Path(LOG_DIR) / "status.log"


def log_event(message):
    """Логування подій у файл та консоль"""
    try:
        # Створюємо директорію для логів, якщо її немає
        Path(LOG_DIR).mkdir(exist_ok=True)

        with open(LOG_FILE, "a", encoding="utf-8") as f:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{timestamp}] {message}\n")
        print(message)
    except Exception as e:
        print(f"Помилка при логуванні: {e}")


def check_proxy(ip, port, timeout=3):
    """Перевірка доступності проксі"""
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        log_event(f"Помилка перевірки проксі {ip}:{port}: {str(e)}")
        return False
    except Exception as e:
        log_event(f"Невідома помилка при перевірці {ip}:{port}: {str(e)}")
        return False


def restart_3proxy():
    """Перезапуск служби 3proxy"""
    try:
        log_event("🔄 Restarting 3proxy service...")
        os.system("sc stop 3proxy")
        time.sleep(3)  # Замість timeout 3
        os.system("sc start 3proxy")
        log_event("✅ 3proxy service restarted successfully")
        return True
    except Exception as e:
        log_event(f"❌ Помилка при перезапуску 3proxy: {str(e)}")
        notify_admin(f"❌ Помилка перезапуску 3proxy: {str(e)}")
        return False


def monitor_proxies():
    """Моніторинг проксі-серверів"""
    while True:
        try:
            data = load_proxies()
            if not data or "active" not in data:
                log_event("❌ Неправильний формат даних проксі")
                time.sleep(60)
                continue

            active = data["active"]
            ip = active.get("ip")
            port = active.get("port")
            http_port = active.get("http_port")

            if not all([ip, port, http_port]):
                log_event("❌ Відсутні обов'язкові параметри проксі")
                time.sleep(60)
                continue

            if check_proxy(ip, port):
                log_event(f"✅ Proxy {ip}:{port} is UP")
            else:
                log_event(f"❌ Proxy {ip}:{port} is DOWN")
                notify_admin(f"❌ Proxy {ip}:{port} впав! Перемикаюся на резервний...")

                if "backup" not in data or not data["backup"]:
                    log_event("❌ Немає резервного проксі для переключення")
                    time.sleep(60)
                    continue

                backup = data["backup"]
                data["active"], data["backup"] = backup, data["active"]

                if not update_config(backup["ip"], backup["port"], backup["http_port"]):
                    log_event("❌ Помилка оновлення конфігурації")
                    continue

                if not save_proxies(data):
                    log_event("❌ Помилка збереження проксі")
                    continue

                if not restart_3proxy():
                    continue

        except Exception as e:
            log_event(f"⛔ Критична помилка: {str(e)}")
            notify_admin(f"⛔ Критична помилка моніторингу: {str(e)}")

        time.sleep(60)

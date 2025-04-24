import requests
import configparser
from pathlib import Path


def notify_admin(message):
    # 1. Використовуємо Path для крос-платформової роботи з шляхами
    config_path = Path("config/telegrambot.cfg")

    # 2. Перевіряємо, чи існує файл конфігурації
    if not config_path.exists():
        print(f"[notifier] Error: Config file not found at {config_path}")
        return False

    # 3. Завантажуємо конфігурацію
    config = configparser.ConfigParser()
    try:
        # 4. Читаємо з явним вказанням кодування
        with open(config_path, "r", encoding="utf-8") as configfile:
            config.read_file(configfile)

        # 5. Додаємо перевірку наявності секції та опцій
        if not config.has_section("telegram"):
            print("[notifier] Error: 'telegram' section not found in config")
            return False

        TOKEN = config.get("telegram", "token")
        CHAT_ID = config.get("telegram", "chat_id")

        # 6. Додаємо timeout для запиту
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}

        try:
            response = requests.post(url, data=data, timeout=10)
            response.raise_for_status()  # 7. Перевіряємо HTTP помилки
            return True
        except requests.exceptions.RequestException as e:
            print(f"[notifier] Telegram API Error: {e}")
            return False

    except configparser.Error as e:
        print(f"[notifier] Config parsing error: {e}")
        return False
    except Exception as e:
        print(f"[notifier] Unexpected error: {e}")
        return False

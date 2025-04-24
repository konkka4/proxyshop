import json
from pathlib import Path

def update_config(ip, port, http_port):
    try:
        # Використовуємо Path для крос-платформової роботи з шляхами
        template_path = Path("config/3proxy_template.cfg")
        output_path = Path("3proxy.cfg")
        
        with open(template_path, "r", encoding='utf-8') as f:
            template = f.read()

        new_config = template.replace("{PORT}", str(port)).replace("{HTTP_PORT}", str(http_port))

        with open(output_path, "w", encoding='utf-8') as f:
            f.write(new_config)
            
    except FileNotFoundError as e:
        print(f"Помилка: файл не знайдено - {e}")
    except Exception as e:
        print(f"Сталася помилка при оновленні конфігурації: {e}")

def load_proxies():
    try:
        proxies_path = Path("data/proxies.json")
        with open(proxies_path, "r", encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Попередження: файл proxies.json не знайдено, повертаємо пустий словник")
        return {}
    except json.JSONDecodeError:
        print("Попередження: помилка парсингу JSON, повертаємо пустий словник")
        return {}
    except Exception as e:
        print(f"Сталася помилка при завантаженні проксі: {e}")
        return {}

def save_proxies(data):
    try:
        proxies_path = Path("data/proxies.json")
        # Створюємо директорію, якщо її немає
        proxies_path.parent.mkdir(exist_ok=True)
        
        with open(proxies_path, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Сталася помилка при збереженні проксі: {e}")
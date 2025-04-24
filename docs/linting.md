# Лінтинг та статична перевірка коду

## Обрані інструменти
| Tool    | Function | Why |
|---------|----------|-----|
| **Black**  | Auto‑format | Opinionated, мінімум конфігів |
| **flake8** | Style + logic errors | Швидкий, розширюється плагінами |
| **mypy**   | Typing | Галузевий стандарт |

## Базові правила
* `line-length = 100`
* Ігнор `E203`, `W503` – рекомендація Black
* `mypy --strict`

## Запуск
```bash
poetry run black .
poetry run flake8
poetry run mypy src

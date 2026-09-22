import re
from services.intents import Intent


EXPENSE_WORDS = [
    "отдал",
    "потратил",
    "купил",
    "заплатил",
]

INCOME_WORDS = [
    "получил",
    "зарплата",
    "пришло",
]


CATEGORIES = {
    "такси": "Транспорт",
    "бензин": "Транспорт",
    "метро": "Транспорт",
    "автобус": "Транспорт",
    "кофе": "Кафе",
    "ресторан": "Кафе",
    "ужин": "Кафе",
    "продукты": "Продукты",
    "магазин": "Покупки",
}


def detect_category(text: str) -> str:
    text = text.lower()

    for word, category in CATEGORIES.items():
        if word in text:
            return category

    return "Другое"


def detect_intent(text: str):
    text = text.lower().strip()

    amount = None

    found = re.findall(r"\d+", text)

    if found:
        amount = int(found[0])

    if "напомни" in text:
        return Intent.REMINDER, {
            "text": text
        }

    if "запиши" in text:
        return Intent.NOTE, {
            "text": text
        }

    if any(word in text for word in EXPENSE_WORDS):
        return Intent.EXPENSE, {
            "amount": amount,
            "category": detect_category(text),
            "text": text,
        }

    if any(word in text for word in INCOME_WORDS):
        return Intent.INCOME, {
            "amount": amount,
            "text": text,
        }

    if "сколько" in text or "статистика" in text:
        return Intent.ANALYTICS, {}

    return Intent.CHAT, {
        "text": text
    }

import re
from services.intents import Intent

expense_words = [
    "отдал","потратил","купил","заплатил"
]

income_words = [
    "получил","зарплата","пришло"
]

def detect_intent(text: str):
    text = text.lower()

    amount = None
    found = re.findall(r"\d+", text)

    if found:
        amount = int(found[0])

    if "напомни" in text:
        return Intent.REMINDER, {"text": text}

    if "запиши" in text:
        return Intent.NOTE, {"text": text}

    if any(w in text for w in expense_words):
        return Intent.EXPENSE, {
            "amount": amount,
            "text": text
        }

    if any(w in text for w in income_words):
        return Intent.INCOME, {
            "amount": amount,
            "text": text
        }

    if "сколько" in text or "статистика" in text:
        return Intent.ANALYTICS, {}

    return Intent.CHAT, {"text": text}

CATEGORIES = {
    "такси":"Транспорт",
    "бензин":"Транспорт",
    "метро":"Транспорт",
    "кофе":"Кафе",
    "ресторан":"Кафе",
    "ужин":"Кафе",
    "продукты":"Продукты",
    "магазин":"Покупки",
}
def detect_category(text):
    text = text.lower()

    for word, category in CATEGORIES.items():
        if word in text:
            return category

    return "Другое"

{
    "amount": amount,
    "category": detect_category(text)
}

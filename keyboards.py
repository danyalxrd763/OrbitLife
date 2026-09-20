from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💰 Мои расходы"),
                KeyboardButton(text="📊 Статистика"),
            ],
            [
                KeyboardButton(text="🗑 Удалить последний"),
                KeyboardButton(text="❓ Помощь"),
            ],
        ],
        resize_keyboard=True,
        input_field_placeholder="Например: Потратил 500 на кофе",
    )

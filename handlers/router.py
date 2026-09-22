from aiogram import Router
from aiogram.types import Message

from services.parser import detect_intent
from services.memory import save_context
from services.intents import Intent


router = Router()


@router.message()
async def orbit_router(message: Message):

    if not message.text:
        return

    intent, data = detect_intent(message.text)

    # Сохраняем контекст последнего действия
    save_context(
        message.from_user.id,
        intent.value,
        data.get("category")
    )

    if intent == Intent.EXPENSE:

        amount = data.get("amount")
        category = data.get("category", "Другое")

        if amount is None:
            await message.answer(
                "💸 Понял, что это расход.\n"
                "Сколько ты потратил?"
            )
            return

        await message.answer(
            f"💸 Записал расход\n\n"
            f"Сумма: {amount} ₽\n"
            f"Категория: {category}"
        )

    elif intent == Intent.INCOME:

        amount = data.get("amount")

        if amount is None:
            await message.answer(
                "💰 Понял, что это доход.\n"
                "Какая сумма?"
            )
            return

        await message.answer(
            f"💰 Записал доход: {amount} ₽"
        )

    elif intent == Intent.REMINDER:

        await message.answer(
            "⏰ Напоминание понял.\n"
            "Механизм времени добавим следующим этапом."
        )

    elif intent == Intent.NOTE:

        await message.answer(
            "📝 Заметка сохранена."
        )

    elif intent == Intent.ANALYTICS:

        await message.answer(
            "📊 Аналитика пока находится в разработке."
        )

    else:

        await message.answer(
            "🤖 Я получил сообщение.\n"
            "Пока не смог определить действие."
        )

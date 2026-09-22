from aiogram import Router
from aiogram.types import Message

from services.parser import detect_intent
from services.memory import save_context
from services.intents import Intent

router = Router()

@router.message()
async def orbit_router(message: Message):

    intent, data = detect_intent(message.text)

    save_context(message.from_user.id, intent, data)

    if intent == Intent.EXPENSE:
        await message.answer(
            f"💸 Записал расход: {data['amount']} ₽"
        )

    elif intent == Intent.INCOME:
        await message.answer(
            f"💰 Доход: {data['amount']} ₽"
        )

    elif intent == Intent.REMINDER:
        await message.answer(
            "⏰ Напоминание понял. Скоро добавим время."
        )

    elif intent == Intent.NOTE:
        await message.answer(
            "📝 Заметка сохранена."
        )

    elif intent == Intent.ANALYTICS:
        await message.answer(
            "📊 Здесь появится аналитика."
        )

    else:
        await message.answer(
            "🤖 Я понял сообщение, но пока не знаю действие."
        )

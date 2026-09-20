import re
from datetime import datetime

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from database import (
    add_expense,
    add_user,
    delete_last_expense,
    get_category_statistics,
    get_expenses,
    get_period_start,
    get_total,
)
from keyboards import main_menu


router = Router()


EXPENSE_PATTERN = re.compile(
    r"^\s*потратил(?:а)?\s+"
    r"(?P<amount>\d+(?:[.,]\d{1,2})?)"
    r"(?:\s*(?:₽|руб(?:лей|ля)?|р))?"
    r"(?:\s+(?:на|за)\s+)?"
    r"(?P<category>.*?)\s*$",
    re.IGNORECASE,
)


def format_amount(amount: float) -> str:
    if amount.is_integer():
        return str(int(amount))

    return f"{amount:.2f}".rstrip("0").rstrip(".")


def parse_expense(text: str):
    match = EXPENSE_PATTERN.match(text)

    if not match:
        return None

    amount = float(match.group("amount").replace(",", "."))
    category = match.group("category").strip()

    if amount <= 0:
        return None

    if not category:
        category = "Другое"

    return amount, category[:50]


def format_date(date_string: str) -> str:
    try:
        date = datetime.fromisoformat(date_string)
        return date.strftime("%d.%m.%Y %H:%M")
    except ValueError:
        return date_string


@router.message(CommandStart())
async def start_handler(message: Message) -> None:
    user = message.from_user

    if user is None:
        return

    await add_user(
        user_id=user.id,
        name=user.first_name or "Пользователь",
    )

    await message.answer(
        "👋 <b>Привет!</b> Я OrbitLife — бот для учёта расходов.\n\n"
        "Пример записи:\n"
        "<code>Потратил 500 на кофе</code>\n\n"
        "Используй кнопки меню или команду /help.",
        reply_markup=main_menu(),
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    await message.answer(
        "<b>Как пользоваться ботом:</b>\n\n"
        "Добавить расход:\n"
        "<code>Потратил 500 на кофе</code>\n"
        "<code>Потратил 1200 на продукты</code>\n\n"
        "Доступные команды:\n"
        "/expenses — последние расходы\n"
        "/stats — статистика\n"
        "/delete — удалить последний расход\n"
        "/help — помощь",
        reply_markup=main_menu(),
    )


@router.message(Command("expenses"))
@router.message(lambda message: message.text == "💰 Мои расходы")
async def expenses_handler(message: Message) -> None:
    user_id = message.from_user.id
    expenses = await get_expenses(user_id)

    if not expenses:
        await message.answer(
            "Расходов пока нет.\n"
            "Напиши, например: <code>Потратил 300 на обед</code>"
        )
        return

    lines = ["<b>Последние расходы:</b>\n"]
    total = 0.0

    for expense in expenses:
        amount = float(expense["amount"])
        total += amount

        lines.append(
            f"• {format_date(expense['created_at'])} — "
            f"{expense['category']}: "
            f"<b>{format_amount(amount)} ₽</b>"
        )

    lines.append(f"\n<b>Итого в списке:</b> {format_amount(total)} ₽")

    await message.answer(
        "\n".join(lines),
        reply_markup=main_menu(),
    )


@router.message(Command("stats"))
@router.message(lambda message: message.text == "📊 Статистика")
async def stats_handler(message: Message) -> None:
    user_id = message.from_user.id

    total = await get_total(user_id)
    today = await get_total(
        user_id,
        get_period_start("today"),
    )
    week = await get_total(
        user_id,
        get_period_start("week"),
    )
    month = await get_total(
        user_id,
        get_period_start("month"),
    )

    categories = await get_category_statistics(user_id)

    text = (
        "<b>📊 Статистика расходов</b>\n\n"
        f"Сегодня: <b>{format_amount(today)} ₽</b>\n"
        f"За 7 дней: <b>{format_amount(week)} ₽</b>\n"
        f"За 30 дней: <b>{format_amount(month)} ₽</b>\n"
        f"Всего: <b>{format_amount(total)} ₽</b>"
    )

    if categories:
        text += "\n\n<b>По категориям:</b>"

        for category in categories:
            text += (
                f"\n• {category['category']}: "
                f"{format_amount(float(category['total']))} ₽"
            )

    await message.answer(
        text,
        reply_markup=main_menu(),
    )


@router.message(Command("delete"))
@router.message(lambda message: message.text == "🗑 Удалить последний")
async def delete_handler(message: Message) -> None:
    deleted = await delete_last_expense(message.from_user.id)

    if deleted:
        await message.answer(
            "✅ Последний расход удалён.",
            reply_markup=main_menu(),
        )
    else:
        await message.answer(
            "Удалять нечего — расходов пока нет.",
            reply_markup=main_menu(),
        )


@router.message(lambda message: message.text == "❓ Помощь")
async def help_button_handler(message: Message) -> None:
    await help_handler(message)


@router.message()
async def text_handler(message: Message) -> None:
    if not message.text:
        return

    parsed = parse_expense(message.text)

    if parsed is None:
        await message.answer(
            "Я не понял сообщение.\n\n"
            "Напиши в формате:\n"
            "<code>Потратил 500 на кофе</code>\n\n"
            "Или нажми «❓ Помощь».",
            reply_markup=main_menu(),
        )
        return

    amount, category = parsed

    await add_user(
        user_id=message.from_user.id,
        name=message.from_user.first_name or "Пользователь",
    )

    await add_expense(
        user_id=message.from_user.id,
        amount=amount,
        category=category,
    )

    await message.answer(
        f"✅ Записал расход:\n"
        f"<b>{category}</b> — {format_amount(amount)} ₽",
        reply_markup=main_menu(),
    )

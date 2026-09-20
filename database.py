from datetime import datetime, timedelta, timezone
from typing import Optional

import aiosqlite


DB_PATH = "orbitlife.db"
db: Optional[aiosqlite.Connection] = None


async def init_db() -> None:
    global db

    db = await aiosqlite.connect(DB_PATH)
    db.row_factory = aiosqlite.Row

    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        """
    )

    await db.execute(
        """
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            amount REAL NOT NULL CHECK(amount > 0),
            category TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
        """
    )

    await db.commit()


async def close_db() -> None:
    global db

    if db is not None:
        await db.close()
        db = None


def get_db() -> aiosqlite.Connection:
    if db is None:
        raise RuntimeError("База данных ещё не инициализирована")

    return db


async def add_user(user_id: int, name: str) -> None:
    database = get_db()

    await database.execute(
        """
        INSERT INTO users (id, name, created_at)
        VALUES (?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET name = excluded.name
        """,
        (
            user_id,
            name,
            datetime.now(timezone.utc).isoformat(),
        ),
    )

    await database.commit()


async def add_expense(
    user_id: int,
    amount: float,
    category: str,
) -> None:
    database = get_db()

    await database.execute(
        """
        INSERT INTO expenses (
            user_id,
            amount,
            category,
            created_at
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            user_id,
            amount,
            category,
            datetime.now(timezone.utc).isoformat(),
        ),
    )

    await database.commit()


async def get_expenses(
    user_id: int,
    limit: int = 20,
):
    database = get_db()

    cursor = await database.execute(
        """
        SELECT id, amount, category, created_at
        FROM expenses
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT ?
        """,
        (user_id, limit),
    )

    return await cursor.fetchall()


async def delete_last_expense(user_id: int) -> bool:
    database = get_db()

    cursor = await database.execute(
        """
        SELECT id
        FROM expenses
        WHERE user_id = ?
        ORDER BY created_at DESC
        LIMIT 1
        """,
        (user_id,),
    )

    expense = await cursor.fetchone()

    if expense is None:
        return False

    await database.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense["id"],),
    )

    await database.commit()
    return True


async def get_total(
    user_id: int,
    start_date: Optional[datetime] = None,
) -> float:
    database = get_db()

    if start_date is None:
        cursor = await database.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = ?
            """,
            (user_id,),
        )
    else:
        cursor = await database.execute(
            """
            SELECT COALESCE(SUM(amount), 0) AS total
            FROM expenses
            WHERE user_id = ?
              AND created_at >= ?
            """,
            (user_id, start_date.isoformat()),
        )

    result = await cursor.fetchone()
    return float(result["total"] or 0)


async def get_category_statistics(user_id: int):
    database = get_db()

    cursor = await database.execute(
        """
        SELECT category, SUM(amount) AS total
        FROM expenses
        WHERE user_id = ?
        GROUP BY category
        ORDER BY total DESC
        """,
        (user_id,),
    )

    return await cursor.fetchall()


def get_period_start(period: str) -> Optional[datetime]:
    now = datetime.now(timezone.utc)

    if period == "today":
        return now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0,
        )

    if period == "week":
        return now - timedelta(days=7)

    if period == "month":
        return now - timedelta(days=30)

    return None

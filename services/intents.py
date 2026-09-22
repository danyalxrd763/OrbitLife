from enum import Enum

class Intent(str, Enum):
    EXPENSE = "expense"
    INCOME = "income"
    REMINDER = "reminder"
    NOTE = "note"
    ANALYTICS = "analytics"
    CHAT = "chat"

memory = {}

def save_context(user_id, intent, data):
    memory[user_id] = {
        "intent": intent,
        "data": data
    }

def get_context(user_id):
    return memory.get(user_id)

import sqlite3

DB = "data/orbitlife.db"

def save_context(user_id, intent, category=None):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    INSERT INTO context_memory(user_id,last_intent,last_category)
    VALUES(?,?,?)
    ON CONFLICT(user_id)
    DO UPDATE SET
        last_intent=excluded.last_intent,
        last_category=excluded.last_category,
        updated_at=CURRENT_TIMESTAMP
    """,(user_id,intent,category))

    conn.commit()
    conn.close()


def get_context(user_id):
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
    SELECT last_intent,last_category
    FROM context_memory
    WHERE user_id=?
    """,(user_id,))

    row = cur.fetchone()
    conn.close()

    return row

CREATE TABLE IF NOT EXISTS context_memory (
    user_id INTEGER PRIMARY KEY,
    last_intent TEXT,
    last_category TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

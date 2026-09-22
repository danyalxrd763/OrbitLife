memory = {}

def save_context(user_id, intent, data):
    memory[user_id] = {
        "intent": intent,
        "data": data
    }

def get_context(user_id):
    return memory.get(user_id)


all_history = []

def add_history(conversation_history: dict):
    all_history.append(conversation_history)
    

def get_history():
    return all_history

def get_history_size():
    print(f"Length of history is ====>>{len(all_history)}")


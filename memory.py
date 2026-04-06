import json
import os

class Memory:
    def __init__(self, filename="history.json"):
        self.filename = filename
        self.history = self.load_history()

    def load_history(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self):
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        if len(self.history) > 20:
            self.history = self.history[-20:]
        self.save_history()

    def get_messages(self, system_prompt):
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.history)
        return messages

    def clear(self):
        self.history = []
        self.save_history()

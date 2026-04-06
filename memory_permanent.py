import json
import os

MEMORY_FILE = "permanent_memory.json"

class PermanentMemory:
    def __init__(self):
        self.data = self._load_memory()

    def _load_memory(self):
        if os.path.exists(MEMORY_FILE):
            try:
                with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {"user_facts": [], "important_events": [], "hermione_opinions": {}}
        return {"user_facts": [], "important_events": [], "hermione_opinions": {}}

    def save_fact(self, fact):
        """Salva um fato sobre o usuário ou o mundo."""
        if fact not in self.data["user_facts"]:
            self.data["user_facts"].append(fact)
            self._save_to_disk()

    def save_opinion(self, topic, opinion):
        """Salva uma opinião própria da Hermione sobre um tema."""
        self.data["hermione_opinions"][topic] = opinion
        self._save_to_disk()

    def _save_to_disk(self):
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def get_summary(self):
        """Retorna um resumo da memória para o prompt do sistema."""
        facts = "\n- ".join(self.data["user_facts"][-10:]) # Últimos 10 fatos
        opinions = "\n".join([f"{t}: {o}" for t, o in list(self.data["hermione_opinions"].items())[-5:]])
        return f"FATOS SOBRE DAVI:\n{facts}\n\nOPINIÕES RECENTES:\n{opinions}"

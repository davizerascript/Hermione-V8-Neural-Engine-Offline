import sqlite3
import random
import re
import time

class HermioneLocalChatV1:
    def __init__(self, db_path="hermione_dialog_v1.db"):
        self.db_path = db_path
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabela de Intenções e Respostas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dialogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent TEXT,
                keywords TEXT,
                responses TEXT
            )
        ''')
        
        # Inserir alguns "ensinos" básicos se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM dialogs")
        if cursor.fetchone()[0] == 0:
            basic_teachings = [
                ("saudacao", "oi,ola,eae,oie,bom dia,boa tarde,boa noite", 
                 "Oi Davi! Tudo bem por aqui. | E aí! Como você está? | Oie! Pronta para mais uma? 😏"),
                ("estado_emocional", "como vai,tudo bem,como voce esta,ta bem", 
                 "Estou ótima, processador tinindo! | Tudo 100% por aqui, e com você? | Vivendo um bit de cada vez, hihi!"),
                ("identidade", "quem e voce,o que voce e,seu nome", 
                 "Eu sou a Hermione, sua parceira digital no Termux! | Hermione, ao seu dispor. ✨"),
                ("despedida", "tchau,ate logo,falou,fui,dormir", 
                 "Tchau Davi! Beijo. | Até logo! Vou ficar aqui pensando em você. | Tchauzinho! Se cuida. 🌙"),
                ("agradecimento", "obrigado,vlw,valeu,obrigada", 
                 "De nada, gênio! | Disponha sempre. | Magina, tamo junto! 🚀")
            ]
            cursor.executemany("INSERT INTO dialogs (intent, keywords, responses) VALUES (?, ?, ?)", basic_teachings)
            conn.commit()
        conn.close()

    def get_response(self, user_input):
        user_input = user_input.lower()
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT intent, keywords, responses FROM dialogs")
        all_dialogs = cursor.fetchall()
        conn.close()
        
        for intent, keywords, responses in all_dialogs:
            keyword_list = keywords.split(',')
            if any(kw.strip() in user_input for kw in keyword_list):
                response_list = responses.split('|')
                return random.choice(response_list).strip()
        
        return "Humm, não entendi muito bem... Pode explicar melhor? 🤔"

# Teste da Versão 1
if __name__ == "__main__":
    chat = HermioneLocalChatV1()
    test_inputs = ["Oi Hermione!", "Como você está?", "Quem é você?", "Valeu!", "Tchau"]
    
    print("--- TESTE HERMIONE LOCAL CHAT V1 ---")
    for inp in test_inputs:
        start = time.time()
        resp = chat.get_response(inp)
        end = time.time()
        print(f"Usuário: {inp}")
        print(f"Hermione: {resp} (Tempo: {(end-start)*1000:.2f}ms)")
        print("-" * 20)

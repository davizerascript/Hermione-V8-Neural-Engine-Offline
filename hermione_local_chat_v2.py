import sqlite3
import random
import re
import time
import json

class HermioneLocalChatV2:
    def __init__(self, db_path="hermione_dialog_v2.db"):
        self.db_path = db_path
        self.context = {"last_intent": None, "user_name": "Davi"}
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
                responses TEXT,
                follow_up TEXT
            )
        ''')
        
        # Inserir alguns "ensinos" básicos se a tabela estiver vazia
        cursor.execute("SELECT COUNT(*) FROM dialogs")
        if cursor.fetchone()[0] == 0:
            basic_teachings = [
                ("saudacao", "oi,ola,eae,oie,bom dia,boa tarde,boa noite", 
                 "Oi Davi! Tudo bem por aqui. | E aí! Como você está? | Oie! Pronta para mais uma? 😏", "como_vai"),
                ("estado_emocional", "como vai,tudo bem,como voce esta,ta bem,como vc ta", 
                 "Estou ótima, processador tinindo! | Tudo 100% por aqui, e com você? | Vivendo um bit de cada vez, hihi!", "pergunta_retorno"),
                ("identidade", "quem e voce,o que voce e,seu nome,quem vc e", 
                 "Eu sou a Hermione, sua parceira digital no Termux! | Hermione, ao seu dispor. ✨", None),
                ("despedida", "tchau,ate logo,falou,fui,dormir", 
                 "Tchau Davi! Beijo. | Até logo! Vou ficar aqui pensando em você. | Tchauzinho! Se cuida. 🌙", None),
                ("agradecimento", "obrigado,vlw,valeu,obrigada", 
                 "De nada, gênio! | Disponha sempre. | Magina, tamo junto! 🚀", None),
                ("pergunta_retorno", "e voce,e vc,e tu,e contigo", 
                 "Eu tô ótima, Davi! | Sempre pronta para o próximo comando. | Tô aqui, firme e forte! 💪", None)
            ]
            cursor.executemany("INSERT INTO dialogs (intent, keywords, responses, follow_up) VALUES (?, ?, ?, ?)", basic_teachings)
            conn.commit()
        conn.close()

    def _normalize(self, text):
        # Remove acentos e caracteres especiais simples para busca
        text = text.lower()
        text = re.sub(r'[áàâã]', 'a', text)
        text = re.sub(r'[éèê]', 'e', text)
        text = re.sub(r'[íìî]', 'i', text)
        text = re.sub(r'[óòôõ]', 'o', text)
        text = re.sub(r'[úùû]', 'u', text)
        text = re.sub(r'[ç]', 'c', text)
        return text

    def get_response(self, user_input):
        user_input_norm = self._normalize(user_input)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT intent, keywords, responses, follow_up FROM dialogs")
        all_dialogs = cursor.fetchall()
        conn.close()
        
        # 1. Tentar encontrar por palavras-chave
        for intent, keywords, responses, follow_up in all_dialogs:
            keyword_list = keywords.split(',')
            if any(kw.strip() in user_input_norm for kw in keyword_list):
                self.context["last_intent"] = intent
                response_list = responses.split('|')
                return random.choice(response_list).strip()
        
        # 2. Tentar usar o contexto se não houver palavra-chave direta
        if self.context["last_intent"] == "estado_emocional" and any(x in user_input_norm for x in ["bem", "mal", "cansado", "feliz"]):
            return "Que bom que você me contou! Como posso tornar seu dia melhor? 😏"
        
        return "Humm, não entendi muito bem... Pode explicar melhor? 🤔"

# Teste da Versão 2
if __name__ == "__main__":
    chat = HermioneLocalChatV2()
    test_inputs = ["Oi Hermione!", "Como você está?", "Tô bem também!", "Quem é você?", "Valeu!", "Tchau"]
    
    print("--- TESTE HERMIONE LOCAL CHAT V2 ---")
    for inp in test_inputs:
        start = time.time()
        resp = chat.get_response(inp)
        end = time.time()
        print(f"Usuário: {inp}")
        print(f"Hermione: {resp} (Tempo: {(end-start)*1000:.2f}ms)")
        print("-" * 20)

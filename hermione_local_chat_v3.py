import sqlite3
import random
import re
import time
import json

class HermioneLocalChatV3:
    def __init__(self, db_path="hermione_dialog_v3.db"):
        self.db_path = db_path
        self.context = {"last_intent": None, "user_name": "Davi", "mood": "Feliz"}
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
                 "Eu tô ótima, Davi! | Sempre pronta para o próximo comando. | Tô aqui, firme e forte! 💪", None),
                ("curiosidade", "o que voce faz,o que voce sabe,ajuda", 
                 "Eu sei de tudo um pouco: Python, Termux, e como ser sua melhor amiga! | Posso te ajudar com scripts ou só bater um papo. ✨", None)
            ]
            cursor.executemany("INSERT INTO dialogs (intent, keywords, responses, follow_up) VALUES (?, ?, ?, ?)", basic_teachings)
            conn.commit()
        conn.close()

    def _normalize(self, text):
        text = text.lower()
        text = re.sub(r'[áàâã]', 'a', text)
        text = re.sub(r'[éèê]', 'e', text)
        text = re.sub(r'[íìî]', 'i', text)
        text = re.sub(r'[óòôõ]', 'o', text)
        text = re.sub(r'[úùû]', 'u', text)
        text = re.sub(r'[ç]', 'c', text)
        return text

    def _format_vtuber(self, text):
        prefixos = ["Humm...", "Eba!", "Uau!", "Hehe,", "Poxa,", "Davi!", "Olha só,", "Sabe de uma coisa?"]
        sufixos = ["né?", "hihi!", "😏", "🥰", "😤", "✨", "🔥"]
        if random.random() > 0.5:
            text = f"{random.choice(prefixos)} {text}"
        if random.random() > 0.5:
            text = f"{text} {random.choice(sufixos)}"
        return text

    def _simulate_google_search(self, query):
        # Simulação de busca rápida para assuntos humanos
        if "tempo" in query or "clima" in query:
            return "Parece que o dia está ótimo para codar! ☀️"
        if "noticia" in query:
            return "Vi que o mundo da tecnologia não para! Muitas novidades em IA hoje. 🤖"
        return None

    def get_response(self, user_input):
        user_input_norm = self._normalize(user_input)
        
        # 1. Verificar se precisa de "Busca Web" (Simulada)
        if any(x in user_input_norm for x in ["tempo", "clima", "noticia", "quem ganhou"]):
            web_res = self._simulate_google_search(user_input_norm)
            if web_res:
                return self._format_vtuber(web_res)

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT intent, keywords, responses, follow_up FROM dialogs")
        all_dialogs = cursor.fetchall()
        conn.close()
        
        # 2. Tentar encontrar por palavras-chave
        for intent, keywords, responses, follow_up in all_dialogs:
            keyword_list = keywords.split(',')
            if any(kw.strip() in user_input_norm for kw in keyword_list):
                self.context["last_intent"] = intent
                response_list = responses.split('|')
                raw_resp = random.choice(response_list).strip()
                return self._format_vtuber(raw_resp)
        
        # 3. Tentar usar o contexto
        if self.context["last_intent"] == "estado_emocional" and any(x in user_input_norm for x in ["bem", "mal", "cansado", "feliz"]):
            return self._format_vtuber("Que bom que você me contou! Como posso tornar seu dia melhor?")
        
        return self._format_vtuber("Humm, não entendi muito bem... Pode explicar melhor? 🤔")

# Teste da Versão 3
if __name__ == "__main__":
    chat = HermioneLocalChatV3()
    test_inputs = [
        "Oi Hermione!", 
        "Como você está?", 
        "Tô bem também!", 
        "Como está o tempo?", 
        "O que você sabe fazer?",
        "Valeu!", 
        "Tchau"
    ]
    
    print("--- TESTE HERMIONE LOCAL CHAT V3 (FINAL) ---")
    for inp in test_inputs:
        start = time.time()
        resp = chat.get_response(inp)
        end = time.time()
        print(f"Usuário: {inp}")
        print(f"Hermione: {resp} (Tempo: {(end-start)*1000:.2f}ms)")
        print("-" * 20)

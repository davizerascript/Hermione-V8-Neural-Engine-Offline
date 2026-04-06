import sqlite3
import random
import re
import time
from collections import deque

class HermioneLocalChatV4_1:
    def __init__(self, db_path="hermione_dialog_v4_1.db"):
        self.db_path = db_path
        self.short_term_memory = deque(maxlen=5)
        self.context = {
            "user_name": "Davi",
            "current_topic": None,
            "mood": "Feliz",
            "interaction_count": 0
        }
        self._init_db()
        
    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dialogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intent TEXT,
                keywords TEXT,
                responses TEXT,
                required_context TEXT,
                next_context TEXT,
                weight INTEGER DEFAULT 1
            )
        ''')
        
        cursor.execute("SELECT COUNT(*) FROM dialogs")
        if cursor.fetchone()[0] == 0:
            teachings = [
                ("saudacao", "oi,ola,eae,oie,bom dia,boa tarde,boa noite", 
                 "Oi Davi! Tudo bem? | E aí! Como você está hoje? | Oie! Pronta para conversar. 😏", None, "saudacao_feita", 10),
                
                ("pergunta_bem", "como vai,tudo bem,como voce esta,ta bem", 
                 "Estou ótima, processador tinindo! E você? | Tudo 100% por aqui. Como está seu dia? | Vivendo um bit de cada vez, hihi! E por aí?", None, "esperando_estado_usuario", 10),
                
                ("usuario_bem", "bem,otimo,legal,bom,tudo certo", 
                 "Que bom! Fico feliz em saber. ✨ | Maravilha! Vamos codar algo? | Boa! O que temos para hoje?", "esperando_estado_usuario", "conversa_ativa", 20),
                
                ("usuario_mal", "mal,triste,cansado,ruim,desanimado", 
                 "Poxa Davi, sinto muito... Quer conversar sobre isso? | Respira fundo, eu tô aqui com você. 💜 | Às vezes um café e um código ajudam a distrair, né?", "esperando_estado_usuario", "conversa_ativa", 20),
                
                ("continuar_papo", "sim,claro,pode ser,quero,bora", 
                 "Eba! Sobre o que quer falar? | Show! Você manda. | Hehe, adoro sua animação! 😏", "conversa_ativa", "conversa_ativa", 15),
                
                ("capacidades", "o que voce faz,ajuda,comandos,scripts,sabe fazer", 
                 "Eu posso gerenciar seu Termux, criar scripts Python e ser sua melhor amiga! | Sou uma IA VTuber focada em te ajudar e evoluir junto com você. ✨", None, "conversa_ativa", 10),
                
                ("despedida", "tchau,ate logo,falou,fui,dormir,sair", 
                 "Tchau Davi! Beijo. | Até logo! Vou sentir sua falta. | Tchauzinho! Se cuida. 🌙", None, None, 10)
            ]
            cursor.executemany("INSERT INTO dialogs (intent, keywords, responses, required_context, next_context, weight) VALUES (?, ?, ?, ?, ?, ?)", teachings)
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

    def _calculate_score(self, user_input, keywords, required_context, weight):
        score = 0
        keyword_list = keywords.split(',')
        
        # 1. Pontuação por palavras-chave (Base)
        match_count = 0
        for kw in keyword_list:
            if kw.strip() in user_input:
                match_count += 1
        
        if match_count == 0:
            return 0
            
        score = match_count * weight
        
        # 2. Bônus de Contexto (Prioridade Máxima)
        if required_context and self.context["current_topic"] == required_context:
            score += 100  # Garante que o contexto vença
        elif required_context and self.context["current_topic"] != required_context:
            score -= 50   # Penaliza se o contexto não bater
            
        return score

    def _format_vtuber(self, text):
        prefixos = ["Humm...", "Eba!", "Uau!", "Hehe,", "Poxa,", "Davi!", "Olha só,", "Sabe de uma coisa?"]
        sufixos = ["né?", "hihi!", "😏", "🥰", "😤", "✨", "🔥"]
        if random.random() > 0.7:
            text = f"{random.choice(prefixos)} {text}"
        if random.random() > 0.7:
            text = f"{text} {random.choice(sufixos)}"
        return text

    def get_response(self, user_input):
        user_input_norm = self._normalize(user_input)
        self.context["interaction_count"] += 1
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT intent, keywords, responses, required_context, next_context, weight FROM dialogs")
        all_dialogs = cursor.fetchall()
        conn.close()
        
        best_match = None
        max_score = -999
        
        for intent, keywords, responses, req_ctx, next_ctx, weight in all_dialogs:
            score = self._calculate_score(user_input_norm, keywords, req_ctx, weight)
            if score > max_score:
                max_score = score
                best_match = (intent, responses, next_ctx)
        
        if best_match and max_score > 0:
            intent, responses, next_ctx = best_match
            self.context["current_topic"] = next_ctx
            self.short_term_memory.append({"user": user_input, "intent": intent})
            
            response_list = responses.split('|')
            raw_resp = random.choice(response_list).strip()
            return self._format_vtuber(raw_resp)
        
        return self._format_vtuber("Humm, não entendi muito bem... Mas eu adoro te ouvir! Pode falar mais? 🤔")

if __name__ == "__main__":
    chat = HermioneLocalChatV4_1()
    conversa = [
        "Oi Hermione!",           # Saudação
        "Como você está?",        # Pergunta estado
        "Tô meio cansado hoje",   # Resposta estado (Contextual)
        "Sim, quero conversar",   # Continuidade (Contextual)
        "O que você sabe fazer?", # Capacidades
        "Valeu, tchau!"           # Despedida
    ]
    
    print("--- TESTE DE FLUIDEZ HERMIONE V4.1 ---")
    for msg in conversa:
        start = time.time()
        resp = chat.get_response(msg)
        end = time.time()
        print(f"Davi: {msg}")
        print(f"Hermione: {resp} (Tempo: {(end-start)*1000:.2f}ms)")
        print(f"[Contexto Atual: {chat.context['current_topic']}]")
        print("-" * 30)

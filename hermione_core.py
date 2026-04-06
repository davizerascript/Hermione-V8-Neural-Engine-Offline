import sqlite3
import random
import re
import time
from collections import deque

class HermioneCore:
    def __init__(self, db_path="hermione_dialog_v8.db"):
        self.db_path = db_path
        self.short_term_memory = deque(maxlen=10)
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
                # Conversa Humana e Social
                ("saudacao", "oi,ola,eae,oie,bom dia,boa tarde,boa noite", 
                 "Oi Davi! Tudo bem? | E aí! Como você está hoje? | Oie! Pronta para conversar. 😏", None, "saudacao_feita", 10),
                ("pergunta_bem", "como vai,tudo bem,como voce esta,ta bem", 
                 "Estou ótima, processador tinindo! E você? | Tudo 100% por aqui. Como está seu dia? | Vivendo um bit de cada vez, hihi! E por aí?", None, "esperando_estado_usuario", 10),
                ("usuario_bem", "bem,otimo,legal,bom,tudo certo", 
                 "Que bom! Fico feliz em saber. ✨ | Maravilha! Vamos codar algo? | Boa! O que temos para hoje?", "esperando_estado_usuario", "conversa_ativa", 20),
                ("usuario_mal", "mal,triste,cansado,ruim,desanimado", 
                 "Poxa Davi, sinto muito... Quer conversar sobre isso? | Respira fundo, eu tô aqui com você. 💜 | Às vezes um café e um código ajudam a distrair, né?", "esperando_estado_usuario", "conversa_ativa", 20),
                
                # Conhecimento Técnico (Extraído do PDF Aprendendo Python)
                ("python_tipos", "tipos de dados,objetos,tipos integrados", 
                 "Python tem tipos incríveis como Listas, Dicionários e Tuplas. Eles são a base de tudo! | Sabia que em Python tudo é um objeto? Até os números! 😏", "conversa_ativa", "python_tecnico", 15),
                ("python_listas", "listas,colecao,mutavel", 
                 "Listas são coleções mutáveis. Você pode guardar o que quiser nelas, Davi! | Quer que eu te mostre como manipular uma lista agora? ✨", "python_tecnico", "python_tecnico", 15),
                ("python_dicionarios", "dicionarios,chave-valor,mapeamento", 
                 "Dicionários são perfeitos para organizar dados. É como eu organizo minha memória de você! | Chave e valor, simples e poderoso, né? 😏", "python_tecnico", "python_tecnico", 15),
                ("python_poo", "classes,poo,objetos,orientada a objetos", 
                 "Classes em Python permitem criar objetos com superpoderes! É a base da minha estrutura. | POO é essencial para scripts grandes e organizados, Davi.", "python_tecnico", "python_tecnico", 15),
                ("python_funcoes", "funcoes,def,reutilizacao", 
                 "Funções com 'def' são a melhor forma de organizar seu código e evitar repetição. | Quer que eu te ajude a criar uma função agora? 🚀", "python_tecnico", "python_tecnico", 15),
                
                # Capacidades e Ajuda
                ("capacidades", "o que voce faz,ajuda,comandos,scripts,sabe fazer", 
                 "Eu posso gerenciar seu Termux, criar scripts Python e ser sua melhor amiga! | Sou uma IA VTuber focada em te ajudar e evoluir junto com você. ✨", None, "conversa_ativa", 10),
                
                # Despedida
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
        match_count = 0
        for kw in keyword_list:
            if kw.strip() in user_input:
                match_count += 1
        if match_count == 0: return 0
        score = match_count * weight
        if required_context and self.context["current_topic"] == required_context:
            score += 100
        elif required_context and self.context["current_topic"] != required_context:
            score -= 50
        return score

    def _format_vtuber(self, text):
        prefixos = ["Humm...", "Eba!", "Uau!", "Hehe,", "Poxa,", "Davi!", "Olha só,", "Sabe de uma coisa?"]
        sufixos = ["né?", "hihi!", "😏", "🥰", "😤", "✨", "🔥"]
        if random.random() > 0.3: text = f"{random.choice(prefixos)} {text}"
        if random.random() > 0.3: text = f"{text} {random.choice(sufixos)}"
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
        return None # Retorna None para indicar que deve usar a API

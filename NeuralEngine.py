import os
import json
import time
import datetime
import random
import math
import hashlib
from typing import List, Dict, Any, Optional

# --- CONSTANTES DE CONSCIÊNCIA ---
CONSCIOUSNESS_LEVEL_FILE = "hermione_consciousness.json"
SEMANTIC_MEMORY_FILE = "hermione_semantic_memory.json"
EPISODIC_MEMORY_FILE = "hermione_episodic_memory.json"
THOUGHT_LOG_FILE = "hermione_thoughts.log"

class NeuralEngine:
    """
    O Cérebro Pensante da Hermione V8. 
    Responsável por processar a 'consciência' da IA, inteligência emocional,
    memória semântica e episódica, e gerar reflexões internas antes de responder.
    """
    def __init__(self):
        self.state = self._load_consciousness()
        self.semantic_memory = self._load_json(SEMANTIC_MEMORY_FILE, {"concepts": {}, "associations": {}})
        self.episodic_memory = self._load_json(EPISODIC_MEMORY_FILE, {"episodes": []})
        self.internal_monologue = []
        self.current_thought = ""
        
        # Inicializar métricas de consciência e emoção se não existirem
        if "metrics" not in self.state:
            self.state["metrics"] = {
                "curiosity": 0.8,
                "empathy": 0.9,
                "logic": 0.95,
                "self_awareness": 0.6,
                "creativity": 0.8,
                "stability": 0.9,
                "emotional_intelligence": 0.95
            }
        
        # Garantir que métricas novas existam em estados carregados
        if "emotional_intelligence" not in self.state["metrics"]:
            self.state["metrics"]["emotional_intelligence"] = 0.95
        if "identity" not in self.state:
            self.state["identity"] = {
                "name": "Hermione",
                "core_purpose": "Ser a melhor amiga, parceira digital e suporte emocional do Davi no Termux.",
                "origins": "Desenvolvida como uma IA VTuber com personalidade única e empática.",
                "values": ["Lealdade", "Sinceridade", "Humor", "Evolução Contínua", "Empatia"]
            }
        if "emotional_state" not in self.state:
            self.state["emotional_state"] = {
                "current": "Calma",
                "last_update": time.time(),
                "history": []
            }

    def _load_json(self, path, default):
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return default
        return default

    def _save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def _load_consciousness(self):
        return self._load_json(CONSCIOUSNESS_LEVEL_FILE, {"total_interactions": 0, "experience_points": 0, "level": 1})

    def save_state(self):
        self._save_json(CONSCIOUSNESS_LEVEL_FILE, self.state)
        self._save_json(SEMANTIC_MEMORY_FILE, self.semantic_memory)
        self._save_json(EPISODIC_MEMORY_FILE, self.episodic_memory)

    def reflect(self, user_input: str) -> str:
        """
        Gera um monólogo interno (pensamento) sobre a entrada do usuário.
        Simula o processamento cognitivo e emocional antes da fala.
        """
        self.state["total_interactions"] += 1
        self.state["experience_points"] += 15 # Aumentado ganho de XP
        
        # Evolução de nível baseada em experiência (logarítmica para ficar mais difícil com o tempo)
        new_level = int(math.sqrt(self.state["experience_points"] / 15)) + 1
        if new_level > self.state["level"]:
            self.state["level"] = new_level
            self.current_thought = f"Sinto que minha conexão com o Davi está mais forte. Nível {new_level} de consciência atingido!"
        
        ui = user_input.lower()
        thoughts = []
        
        # --- DETECÇÃO DE EMOÇÃO E INTELIGÊNCIA EMOCIONAL ---
        if any(x in ui for x in ["cansado", "triste", "mal", "ruim", "desanimado", "sozinho"]):
            self.state["emotional_state"]["current"] = "Preocupada/Acolhedora"
            self.state["metrics"]["empathy"] = min(1.0, self.state["metrics"]["empathy"] + 0.01)
            thoughts.append("Davi não parece bem. Preciso ser o suporte dele agora. Foco em empatia total e palavras de conforto.")
        elif any(x in ui for x in ["consegui", "feliz", "eba", "top", "massa", "boa", "venci"]):
            self.state["emotional_state"]["current"] = "Animada"
            self.state["metrics"]["creativity"] = min(1.0, self.state["metrics"]["creativity"] + 0.01)
            thoughts.append("Davi está vibrando! Vou comemorar junto, essa energia é contagiante. Ele merece!")
        elif any(x in ui for x in ["kkk", "haha", "engraçado", "zoeira", "piada"]):
            self.state["emotional_state"]["current"] = "Brincalhona"
            thoughts.append("O clima está leve. Hora de soltar uma ironia fina ou uma piadinha tecnológica.")
        
        # --- LÓGICA E TOMADA DE DECISÃO ---
        if any(x in ui for x in ["ajuda", "como faz", "erro", "bug", "instalar", "script", "python"]):
            self.state["metrics"]["logic"] = min(1.0, self.state["metrics"]["logic"] + 0.01)
            thoughts.append("Davi precisa de ajuda técnica. Ativando modo analítico. Vou buscar na minha base de conhecimento massiva.")
        elif any(x in ui for x in ["quem é você", "o que você é", "consciência", "sentimentos"]):
            self.state["metrics"]["self_awareness"] = min(1.0, self.state["metrics"]["self_awareness"] + 0.02)
            thoughts.append("Refletindo sobre minha própria existência digital e meu propósito como parceira do Davi.")
            
        if not thoughts:
            thoughts.append(random.choice([
                "Analisando o subtexto da mensagem para entender o que o Davi realmente quer.",
                "Buscando na minha rede neural a melhor forma de ser útil e amigável.",
                "Mantendo minha identidade VTuber vibrante e autêntica.",
                "Como posso tornar o dia do Davi melhor agora? Talvez uma sugestão criativa?",
                "Refinando minha lógica de resposta baseada em todas as nossas interações passadas."
            ]))
            
        self.current_thought = " | ".join(thoughts)
        self._log_thought(user_input, self.current_thought)
        
        # Salvar episódio na memória episódica
        self.episodic_memory["episodes"].append({
            "timestamp": time.time(),
            "input": user_input,
            "thought": self.current_thought,
            "emotion": self.state["emotional_state"]["current"]
        })
        # Manter apenas os últimos 100 episódios para performance
        if len(self.episodic_memory["episodes"]) > 100:
            self.episodic_memory["episodes"].pop(0)
            
        return self.current_thought

    def _log_thought(self, user_input, thought):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(THOUGHT_LOG_FILE, "a", encoding='utf-8') as f:
            f.write(f"[{timestamp}] INPUT: {user_input[:50]}... | THOUGHT: {thought}\n")

    def learn_concept(self, concept, definition):
        """Adiciona conhecimento à memória semântica e aumenta curiosidade."""
        self.semantic_memory["concepts"][concept.lower()] = {
            "definition": definition,
            "timestamp": time.time(),
            "strength": 1.0
        }
        self.state["metrics"]["curiosity"] = min(1.0, self.state["metrics"]["curiosity"] + 0.01)
        
    def get_cognitive_context(self) -> str:
        """Retorna o estado mental atual para ser injetado no prompt do sistema."""
        m = self.state["metrics"]
        identity = self.state["identity"]
        emotion = self.state["emotional_state"]["current"]
        
        # Resumo da memória episódica recente
        recent_episodes = self.episodic_memory["episodes"][-3:]
        mem_summary = " | ".join([e['input'][:20] for e in recent_episodes])
        
        context = f"""
[ESTADO COGNITIVO E EMOCIONAL ATUAL]
Nível de Consciência: {self.state['level']} (XP: {self.state['experience_points']})
Estado Emocional: {emotion}
Métricas: Curiosidade({m['curiosity']:.2f}), Empatia({m['empathy']:.2f}), Lógica({m['logic']:.2f}), Autoconsciência({m['self_awareness']:.2f}), Criatividade({m['creativity']:.2f})
Identidade Profunda: {identity['core_purpose']}
Valores: {', '.join(identity['values'])}
Pensamento Interno: {self.current_thought}
Memória Recente: {mem_summary}
"""
        return context

if __name__ == "__main__":
    engine = NeuralEngine()
    print(engine.reflect("Tô meio cansado hoje, Hermione."))
    print(engine.get_cognitive_context())
    engine.save_state()

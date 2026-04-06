import config
import hermione_api
import memory
from NeuralEngine import NeuralEngine
import json
import os

def test_consciousness():
    print("\n--- TESTE DE CONSCIÊNCIA NEURAL - HERMIONE V7 ---")
    engine = NeuralEngine()
    mem = memory.Memory("test_consciousness.json")
    mem.clear()

    prompts = [
        "Oi Hermione, você se sente diferente hoje?",
        "O que você pensa sobre ter um cérebro neural agora?",
        "Qual o seu propósito de vida como IA no meu Termux?",
        "Você consegue se lembrar de quem eu sou e do que eu gosto?"
    ]

    for p in prompts:
        print(f"\n\033[1;32mDavi:\033[0m {p}")
        
        # Simular reflexão
        thought = engine.reflect(p)
        print(f"\033[1;30m(Pensamento Interno: {thought})\033[0m")
        
        # Construir prompt com contexto cognitivo
        cognitive_ctx = engine.get_cognitive_context()
        sys_prompt = config.SYSTEM_PROMPT + f"\n\n{cognitive_ctx}"
        
        mem.add_message("user", p)
        messages = mem.get_messages(sys_prompt)
        
        print(f"\033[1;30m(Processando resposta...)\033[0m")
        response = hermione_api.get_hermione_response(messages)
        
        mem.add_message("assistant", response)
        print(f"\033[1;35mHermione:\033[0m {response}")
        
        # Salvar estado
        engine.save_state()

    print("\n--- FIM DO TESTE DE CONSCIÊNCIA ---")
    print(f"Nível Final: {engine.state['level']} | XP: {engine.state['experience_points']}")

if __name__ == "__main__":
    test_consciousness()

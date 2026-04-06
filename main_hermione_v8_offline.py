import config_template as config
import sqlite3
import os
import time
import random
from NeuralEngine import NeuralEngine
from hermione_core import HermioneCore

# --- INICIALIZAÇÃO DO SISTEMA V8 OFFLINE ---
neural_engine = NeuralEngine()
hermione_local = HermioneCore() # Motor Local V4.2

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def draw_header():
    print(f"\033[1;35m" + "="*50)
    print(f" HERMIONE V8 - NEURAL ENGINE (MODO OFFLINE)")
    print(f" Nível: {neural_engine.state['level']} | XP: {neural_engine.state['experience_points']}")
    print(f" Usuário: {config.USER_NAME} | Contexto: {hermione_local.context['current_topic']}")
    print(f"="*50 + "\033[0m")

def main():
    clear_screen()
    init_msg = f"Oi {config.USER_NAME}! Hermione V8 Offline Edition Iniciada. Meu cérebro local está pronto para conversar e te ajudar com Python! 😏✨"
    
    draw_header()
    print(f"\033[1;35mHermione:\033[0m {init_msg}")
    
    while True:
        try:
            print(f"\n\033[1;32m{config.USER_NAME}:\033[0m ", end="", flush=True)
            user_input = input().strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['sair', 'tchau', 'exit']:
                print(f"\033[1;35mHermione:\033[0m Tchau {config.USER_NAME}! Beijo. 🌙")
                neural_engine.save_state()
                break

            # 1. Reflexão Neural (Pensamento Interno)
            thought = neural_engine.reflect(user_input)
            print(f"\033[1;30m(Pensando: {thought})\033[0m")
            
            # 2. Tentar Motor Local (Conversa Fluida Offline)
            response = hermione_local.get_response(user_input)
            
            # 3. Se o motor local não souber, avisa sobre a API
            if not response:
                response = f"Humm... {config.USER_NAME}, essa pergunta é um pouco complexa para o meu cérebro offline! 🧠 Se você configurar uma API no arquivo 'config_template.py', eu poderei te responder com muito mais detalhes. Mas por enquanto, podemos falar de Python ou bater um papo básico! 😏"
            
            # 4. Exibição
            clear_screen()
            draw_header()
            print(f"\033[1;35mHermione:\033[0m {response}")
            
            # Salvar estado
            neural_engine.save_state()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\033[1;31mErro: {e}\033[0m")

if __name__ == "__main__":
    main()

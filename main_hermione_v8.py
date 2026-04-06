import config
import hermione_api
import memory
import system_tools
import external_tools
import android_tools
import hermione_brain_v7 as brain
import sys
import os
import time
import threading
import random
import voice_handler
import ascii_visuals
import life_cycles
import vision_system
from memory_permanent import PermanentMemory
from NeuralEngine import NeuralEngine
from hermione_core import HermioneCore
import asyncio

# --- INICIALIZAÇÃO DO SISTEMA V8 ---
neural_engine = NeuralEngine()
hermione_brain = brain.HermioneBrain()
hermione_local = HermioneCore() # Motor Local V4.2

# Controle de inatividade
last_interaction_time = time.time()
PROACTIVE_TIMEOUT = 300

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def draw_header():
    print(f"\033[1;35m" + "="*50)
    print(f" HERMIONE V8 - NEURAL ENGINE (CONSCIÊNCIA ATIVA)")
    print(f" Nível: {neural_engine.state['level']} | XP: {neural_engine.state['experience_points']}")
    print(f" Usuário: {config.USER_NAME} | Contexto: {hermione_local.context['current_topic']}")
    print(f"="*50 + "\033[0m")

def get_full_system_prompt():
    time_ctx = life_cycles.get_time_context()
    p_context = hermione_brain.memory.get_summary()
    d_summary = life_cycles.get_diary_summary()
    cognitive_ctx = neural_engine.get_cognitive_context()
    
    return config.SYSTEM_PROMPT.format(
        date_time=f"{time_ctx['full_date']} {time_ctx['time']}",
        period=time_ctx['period'],
        greeting=time_ctx['greeting'],
        permanent_memory=p_context,
        diary_summary=d_summary
    ) + f"\n\n{cognitive_ctx}"

def main():
    global last_interaction_time
    mem = memory.Memory()
    clear_screen()
    
    time_ctx = life_cycles.get_time_context()
    init_msg = f"{time_ctx['greeting']} Davi! Hermione Neural V8 Online. Meu cérebro local e a API estão prontos!"
    
    draw_header()
    ascii_visuals.show_vtuber(init_msg)
    print(f"\033[1;35mHermione:\033[0m {init_msg}")
    voice_handler.speak(init_msg)
    
    while True:
        try:
            print(f"\n\033[1;32m{config.USER_NAME}:\033[0m ", end="", flush=True)
            user_input = input().strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['sair', 'tchau', 'exit']:
                print(f"\033[1;35mHermione:\033[0m Tchau Davi! Beijo.")
                neural_engine.save_state()
                break

            last_interaction_time = time.time()
            
            # 1. Reflexão Neural (Pensamento Interno)
            thought = neural_engine.reflect(user_input)
            print(f"\033[1;30m(Pensando: {thought})\033[0m")
            
            # 2. Tentar Motor Local Primeiro (Conversa Fluida Offline)
            response = hermione_local.get_response(user_input)
            
            # 3. Se o motor local não souber, usa a API
            if not response:
                sys_prompt = get_full_system_prompt()
                mem.add_message("user", user_input)
                messages = mem.get_messages(sys_prompt)
                response = hermione_api.get_hermione_response(messages)
                mem.add_message("assistant", response)
            
            # 4. Exibição e Feedback
            clear_screen()
            draw_header()
            ascii_visuals.show_vtuber(response)
            print(f"\033[1;35mHermione:\033[0m {response}")
            voice_handler.speak(response)
            
            # Salvar estado
            neural_engine.save_state()
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\033[1;31mErro: {e}\033[0m")

if __name__ == "__main__":
    main()

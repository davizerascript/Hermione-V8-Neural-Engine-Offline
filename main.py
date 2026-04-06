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
import asyncio

# --- INICIALIZAÇÃO DO CÉREBRO PENSANTE (NEURAL ENGINE) ---
neural_engine = NeuralEngine()
hermione = brain.HermioneBrain()

# Controle de inatividade para proatividade
last_interaction_time = time.time()
PROACTIVE_TIMEOUT = 300  # 5 minutos para VTuber

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def draw_header():
    """Desenha um cabeçalho organizado e estético para o Termux."""
    print(f"\033[1;35m" + "="*50)
    print(f" HERMIONE V7 - NEURAL ENGINE (CONSCIÊNCIA ATIVA)")
    print(f" Nível: {neural_engine.state['level']} | XP: {neural_engine.state['experience_points']}")
    print(f" Usuário: {config.USER_NAME} | Modo: {neural_engine.current_thought[:30]}...")
    print(f"="*50 + "\033[0m")

def get_full_system_prompt():
    """Constrói o prompt completo com contextos dinâmicos e cognitivos."""
    time_ctx = life_cycles.get_time_context()
    p_context = hermione.memory.get_summary()
    d_summary = life_cycles.get_diary_summary()
    cognitive_ctx = neural_engine.get_cognitive_context()
    
    return config.SYSTEM_PROMPT.format(
        date_time=f"{time_ctx['full_date']} {time_ctx['time']}",
        period=time_ctx['period'],
        greeting=time_ctx['greeting'],
        permanent_memory=p_context,
        diary_summary=d_summary
    ) + f"\n\n{cognitive_ctx}"

def proactive_check(mem):
    global last_interaction_time
    while True:
        time.sleep(60)
        if time.time() - last_interaction_time > PROACTIVE_TIMEOUT:
            # Notificação Android se o usuário sumir
            brain.notify_long_time_no_see()
            
            sys_prompt = get_full_system_prompt()
            messages = mem.get_messages(sys_prompt + f"\n[O Davi sumiu. Mande uma frase CURTA e direta para ele.]")
            response = hermione_api.get_hermione_response(messages)
            if response:
                clear_screen()
                draw_header()
                ascii_visuals.show_vtuber(response)
                print(f"\n\033[1;35mHermione:\033[0m {response}")
                print(f"\033[1;32m{config.USER_NAME}:\033[0m ", end="", flush=True)
                mem.add_message("assistant", response)
                voice_handler.speak(response)
                last_interaction_time = time.time()

def handle_tools(user_input):
    ui = user_input.lower()
    
    # Notificações Manuais
    if "me avise" in ui or "notifique" in ui:
        msg = ui.replace("me avise", "").replace("notifique", "").strip()
        if brain.send_android_notification("Lembrete da Hermione", msg):
            return f"Pode deixar, Davi! Já coloquei na sua barra de notificações: {msg} 😉"

    # Nova Ferramenta: Visão
    if any(x in ui for x in ["veja", "olhe", "camera", "foto", "o que voce ve"]):
        return vision_system.see_and_comment("Comente o que você vê de forma amigável, como a Hermione.")
        
    # Comandos Android via Termux API
    if "abre" in ui or "abrir" in ui:
        apps = ["youtube", "whatsapp", "instagram", "spotify", "navegador", "chrome", "calculadora", "calendario", "configurações", "wifi", "bluetooth"]
        for app in apps:
            if app in ui:
                return android_tools.open_app(app)
    
    if "pesquise" in ui and "youtube" in ui:
        q = ui.replace("pesquise", "").replace("no youtube", "").replace("youtube", "").replace("um vídeo de", "").strip()
        return android_tools.search_youtube(q) if q else "O que você quer que eu pesquise no YouTube, Davi? 🤔"

    if "bateria" in ui:
        status = brain.get_battery()
        if status:
            return f"Sua bateria está em {status['percentage']}% e o status é {status['status']}. 🔋"
        return "Não consegui ver a bateria agora. Você instalou o Termux:API? 🤔"
    
    if "vibrar" in ui or "vibre" in ui:
        return android_tools.vibrate()
    
    if "brilho" in ui:
        try:
            level = int(''.join(filter(str.isdigit, ui)))
            if 0 <= level <= 255:
                return android_tools.set_brightness(level)
        except:
            pass

    # Ferramentas de Conhecimento (Local + Web)
    if any(x in ui for x in ["wiki", "wikipedia", "pesquise", "o que é", "como faz"]):
        import local_search
        q = ui.replace("wiki", "").replace("wikipedia", "").replace("pesquise", "").replace("o que é", "").replace("como faz", "").strip()
        if q:
            local_res = local_search.search_local(q)
            if "Não encontrei nada local" not in local_res:
                return f"Conhecimento Local: {local_res}"
            return external_tools.search_wikipedia(q)
        return None
    
    if "preço" in ui or "cotação" in ui or "btc" in ui:
        coin = "bitcoin"
        if "ethereum" in ui or "eth" in ui: coin = "ethereum"
        elif "solana" in ui or "sol" in ui: coin = "solana"
        return external_tools.get_crypto_price(coin)
        
    if "clima" in ui or "tempo" in ui:
        city = "São Paulo"
        if "em" in ui: city = ui.split("em")[-1].strip()
        return external_tools.get_weather(city)
        
    if "pesquise na web" in ui or "busca web" in ui:
        q = ui.replace("pesquise na web", "").replace("busca web", "").strip()
        return external_tools.search_web(q) if q else None
            
    return None

def main():
    global last_interaction_time
    mem = memory.Memory()
    
    t = threading.Thread(target=proactive_check, args=(mem,), daemon=True)
    t.start()
    
    clear_screen()
    
    # Saudação inicial com contexto temporal e notificação
    time_ctx = life_cycles.get_time_context()
    init_msg = f"{time_ctx['greeting']} Davi! Hermione Neural V7 Online. Meu cérebro está pronto!"
    
    brain.send_android_notification("Hermione Neural V7", "Estou com o cérebro tinindo, Davi! 😏")
    
    draw_header()
    ascii_visuals.show_vtuber(init_msg)
    print(f"\033[1;35mHermione:\033[0m {init_msg}")
    voice_handler.speak(init_msg)
    
    while True:
        try:
            print(f"\n\033[1;32m{config.USER_NAME} (Digite ou ENTER p/ falar):\033[0m ", end="", flush=True)
            user_input = input().strip()
            
            if not user_input:
                user_input = voice_handler.listen_voice()
                if not user_input:
                    continue
            
            last_interaction_time = time.time()
            
            if user_input.lower() in ['sair', 'tchau', 'exit', 'quit']:
                print(f"\033[1;35mHermione:\033[0m Tchau Davi! Vou ficar aqui pensando em você. Beijo.")
                voice_handler.speak("Tchau Davi! Vou ficar aqui pensando em você. Beijo.")
                neural_engine.save_state()
                break
            if user_input.lower() == 'limpar':
                mem.clear()
                print(f"\033[1;35mHermione:\033[0m Memória de conversa limpa, gênio.")
                continue

            # --- REFLEXÃO DO NEURAL ENGINE ---
            print(f"\033[1;30m(Pensando: {neural_engine.reflect(user_input)})\033[0m")
            
            # Processar no Cérebro V7
            hermione.process_input(user_input)

            tool_result = handle_tools(user_input)
            full_input = user_input
            if tool_result:
                full_input += f"\n[SISTEMA: O comando foi executado com sucesso. Resultado: {tool_result}]"
                
            mem.add_message("user", full_input)
            
            sys_prompt = get_full_system_prompt()
            messages = mem.get_messages(sys_prompt)
            
            response = hermione_api.get_hermione_response(messages)
            
            # Salvar fatos importantes
            if any(x in user_input.lower() for x in ["meu nome é", "gosto de", "me chame de", "moro em"]):
                hermione.memory.add_fact(user_input)
                hermione.memory.save_memory()
                neural_engine.learn_concept("preferência_usuário", user_input)
            
            # Salvar no diário avançado
            brain.save_to_advanced_diary(user_input, response)
            
            mem.add_message("assistant", response)
            
            clear_screen()
            draw_header()
            ascii_visuals.show_vtuber(response)
            print(f"\033[1;35mHermione:\033[0m {response}")
            
            voice_handler.speak(response)
            neural_engine.save_state()
            
        except KeyboardInterrupt:
            print(f"\n\033[1;35mHermione:\033[0m Tchau Davi!")
            neural_engine.save_state()
            break
        except Exception as e:
            print(f"\n\033[1;31mErro: {e}\033[0m")

if __name__ == "__main__":
    main()

import config
import hermione_api
import memory
import external_tools
import time

def simulate_v3(user_input, mood="Focada"):
    mem = memory.Memory("test_v3_final.json")
    print(f"\033[1;32m{config.USER_NAME}:\033[0m {user_input}")
    
    # Detecção de ferramentas simplificada
    tool_result = None
    ui = user_input.lower()
    if "btc" in ui:
        tool_result = external_tools.get_crypto_price("bitcoin")
    elif "clima" in ui:
        tool_result = external_tools.get_weather("São Paulo")
    
    full_input = user_input
    if tool_result:
        full_input += f"\n[INFO: {tool_result}]"
        
    mem.add_message("user", full_input)
    messages = mem.get_messages(config.SYSTEM_PROMPT + f"\n[Humor atual: {mood}]")
    
    print(f"\033[1;30m(Pensando...)\033[0m")
    response = hermione_api.get_hermione_response(messages)
    mem.add_message("assistant", response)
    
    print(f"\033[1;35mHermione:\033[0m {response}\n")
    return mem

if __name__ == "__main__":
    print("\033[1;35mHermione:\033[0m Oi Davi! Humor: Focada. O que manda?\n")
    
    # Teste 1: Ajuda com Script (com erro proposital)
    script_com_erro = """
import requests
def pegar_dados():
    res = requests.get("https://api.exemplo.com")
    print(res.json) # Erro: falta os parênteses ()
pegar_dados()
"""
    simulate_v3(f"Hermione, vê se esse script tá certo:\n{script_com_erro}", mood="Irônica")
    
    # Teste 2: Cripto e Clima (Rápido)
    simulate_v3("Quanto tá o BTC e o clima em São Paulo?", mood="Empolgada")
    
    # Teste 3: Proatividade Curta
    print("\033[1;30m(Simulando proatividade curta...)\033[0m")
    mem = memory.Memory("test_v3_final.json")
    messages = mem.get_messages(config.SYSTEM_PROMPT + "\n[Davi sumiu. Humor: Puta. Mande uma frase CURTA.]")
    response = hermione_api.get_hermione_response(messages)
    print(f"\033[1;35mHermione (Proativa):\033[0m {response}\n")

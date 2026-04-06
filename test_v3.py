import config
import hermione_api
import memory
import external_tools
import time

def simulate_v3(user_input):
    mem = memory.Memory("test_v3_history.json")
    print(f"\033[1;32m{config.USER_NAME}:\033[0m {user_input}")
    
    # Detecção de ferramentas simplificada para o teste
    tool_result = None
    ui = user_input.lower()
    if "preço" in ui or "btc" in ui:
        tool_result = external_tools.get_crypto_price("bitcoin")
    elif "clima" in ui:
        tool_result = external_tools.get_weather("São Paulo")
    
    full_input = user_input
    if tool_result:
        full_input += f"\n[INFO: {tool_result}]"
        
    mem.add_message("user", full_input)
    messages = mem.get_messages(config.SYSTEM_PROMPT + "\n[Humor atual: Irônica]")
    
    print(f"\033[1;30m(Pensando...)\033[0m")
    response = hermione_api.get_hermione_response(messages)
    mem.add_message("assistant", response)
    
    print(f"\033[1;35mHermione:\033[0m {response}\n")

if __name__ == "__main__":
    print("\033[1;35mHermione:\033[0m Oi Davi! Humor: Focada. O que manda?\n")
    
    # Teste 1: Fala curta e direta
    simulate_v3("O que você acha de eu criar um bot de spam no WhatsApp?")
    
    # Teste 2: Cripto
    simulate_v3("Qual o preço do BTC hoje?")
    
    # Teste 3: Clima
    simulate_v3("Como tá o clima em São Paulo?")

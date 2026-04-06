import config
import hermione_api
import memory
import external_tools
import time

def simulate_chat(user_input):
    mem = memory.Memory("test_drive_history.json")
    print(f"\033[1;32m{config.USER_NAME}:\033[0m {user_input}")
    
    # Simular detecção de ferramentas
    tool_result = None
    if "wiki" in user_input.lower():
        query = user_input.lower().replace("wiki", "").replace("wikipedia", "").replace("pesquise", "").strip()
        tool_result = external_tools.search_wikipedia(query)
    
    full_input = user_input
    if tool_result:
        full_input += f"\n[RESULTADO DA FERRAMENTA: {tool_result}]"
        
    mem.add_message("user", full_input)
    messages = mem.get_messages(config.SYSTEM_PROMPT)
    
    print(f"\033[1;30m(Hermione está pensando...)\033[0m")
    response = hermione_api.get_hermione_response(messages)
    mem.add_message("assistant", response)
    
    print(f"\033[1;35mHermione:\033[0m {response}\n")
    return mem

def simulate_proactive(mem):
    print(f"\033[1;30m(Simulando silêncio do Davi...)\033[0m")
    messages = mem.get_messages(config.SYSTEM_PROMPT + "\n[O Davi está em silêncio faz um tempo. Mande uma mensagem curta, provocativa ou curiosa para puxar assunto.]")
    response = hermione_api.get_hermione_response(messages)
    print(f"\033[1;35mHermione (Proativa):\033[0m {response}\n")

if __name__ == "__main__":
    print("\033[1;35mHermione:\033[0m Oi Davi! Já tava com saudade. O que vamos aprontar no Termux hoje?\n")
    
    # Teste 1: Personalidade e Opinião
    mem = simulate_chat("Hermione, o que você acha de eu passar a noite inteira codando scripts pro Termux em vez de dormir?")
    
    # Teste 2: Ferramenta Wikipedia
    simulate_chat("Hermione, pesquise sobre a história da Tecnologia na wiki pra mim.")
    
    # Teste 3: Proatividade
    simulate_proactive(mem)

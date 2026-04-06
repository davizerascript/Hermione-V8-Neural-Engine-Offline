import config
import hermione_api
import memory
import android_tools
import os

def test_spontaneous_modes():
    print("\n--- Testando Modos Espontâneos ---")
    mem = memory.Memory()
    sys_prompt = config.SYSTEM_PROMPT.format(
        date_time="05/04/2026 14:00",
        period="Tarde",
        greeting="Boa tarde",
        permanent_memory="Davi gosta de animes e está criando uma IA no Termux.",
        diary_summary="Nenhuma interação recente."
    )
    
    test_cases = [
        "Oi Hermione, tudo bem? O que você está fazendo?",
        "Hermione, me ajuda com um código em Python para ler um JSON?",
        "Nossa, você é muito chata às vezes, sabia? Hahaha",
        "Tô meio triste hoje, as coisas não estão dando muito certo..."
    ]
    
    for msg in test_cases:
        print(f"\nDavi: {msg}")
        mem.add_message("user", msg)
        messages = mem.get_messages(sys_prompt)
        response = hermione_api.get_hermione_response(messages)
        print(f"Hermione: {response}")
        mem.add_message("assistant", response)

def test_android_commands():
    print("\n--- Testando Comandos Android ---")
    test_inputs = [
        "Hermione, abre o youtube pra mim",
        "Pesquise um vídeo de gato no youtube",
        "Como está minha bateria?",
        "Faz o celular vibrar um pouco"
    ]
    
    from main import handle_tools
    
    for ui in test_inputs:
        print(f"\nInput: {ui}")
        result = handle_tools(ui)
        print(f"Resultado do Comando: {result}")

if __name__ == "__main__":
    # Nota: O teste de API requer uma chave válida. 
    # Como estou no ambiente sandbox, vou simular ou apenas verificar a lógica se a chave não funcionar.
    try:
        test_android_commands()
        test_spontaneous_modes()
    except Exception as e:
        print(f"Erro durante os testes: {e}")

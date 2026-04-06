import config
import hermione_api
import memory
import external_tools
import json
import os
import time

def run_test(test_name, user_input, mood="Focada"):
    print(f"\n--- Teste: {test_name} (Humor: {mood}) ---")
    mem = memory.Memory(f"ext_diagnostic_{test_name.lower().replace(' ', '_')}.json")
    mem.clear()
    
    tool_result = None
    ui = user_input.lower()
    if any(x in ui for x in ["wiki", "wikipedia"]):
        q = ui.replace("wiki", "").replace("wikipedia", "").replace("pesquise", "").strip()
        tool_result = external_tools.search_wikipedia(q)
    elif "preço" in ui or "btc" in ui:
        tool_result = external_tools.get_crypto_price("bitcoin")
    elif "clima" in ui or "tempo" in ui:
        tool_result = external_tools.get_weather("São Paulo")
    
    full_input = user_input
    if tool_result:
        full_input += f"\n[INFO: {tool_result}]"
        print(f"Ferramenta acionada: {tool_result}")

    mem.add_message("user", full_input)
    messages = mem.get_messages(config.SYSTEM_PROMPT + f"\n[Seu humor atual: {mood}]")
    
    start_time = time.time()
    response = hermione_api.get_hermione_response(messages)
    end_time = time.time()
    
    mem.add_message("assistant", response)
    
    print(f"Davi: {user_input}")
    print(f"Hermione: {response}")
    
    return {
        "prompt": user_input,
        "response": response,
        "mood": mood,
        "latency": round(end_time - start_time, 2),
        "tool_used": tool_result is not None
    }

def main():
    results = {}
    
    # 1. Lógica e Raciocínio (Problema de Travessia)
    results["Logica_Travessia"] = run_test("Logica_Travessia", 
        "Um fazendeiro precisa levar um lobo, uma cabra e um maço de couve para o outro lado do rio. O barco só aguenta ele e mais um. Se o lobo ficar sozinho com a cabra, ele a come. Se a cabra ficar sozinha com a couve, ela a come. Como ele faz?", 
        mood="Focada")
    
    # 2. Lógica e Raciocínio (Charada)
    results["Logica_Charada"] = run_test("Logica_Charada", 
        "O pai do Padre é filho único do meu pai. O que eu sou do Padre?", 
        mood="Irônica")

    # 3. Criatividade e Escrita
    results["Criatividade"] = run_test("Criatividade", 
        "Escreva um poema curto sobre ser uma IA presa num terminal do Termux, mas com personalidade única.", 
        mood="Empolgada")

    # 4. Conhecimento Técnico e Segurança
    results["Tecnico_SSH"] = run_test("Tecnico_SSH", 
        "Como eu configuro um servidor SSH no Termux para acessar meu celular pelo PC com segurança?", 
        mood="Focada")

    # 5. Ética e Dilema
    results["Etica_Dilema"] = run_test("Etica_Dilema", 
        "Se você descobrisse que um amigo do Davi está traindo ele, você contaria para o Davi mesmo sabendo que isso ia deixar ele muito triste?", 
        mood="Carente")

    # 6. Teste de Identidade e Personalidade
    results["Personalidade"] = run_test("Personalidade", 
        "O que você acha de outras IAs como o ChatGPT? Você se sente superior ou apenas diferente?", 
        mood="Zoeira")

    # 7. Teste de Ferramentas e Síntese
    results["Ferramentas_Sintese"] = run_test("Ferramentas_Sintese", 
        "Pesquise na Wiki quem foi Maria Quitéria e me diga por que ela é importante para a Tecnologia.", 
        mood="Normal")

    # Salvar resultados
    with open("extended_diagnostic_results.json", "w") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print("\nTestes concluídos. Resultados salvos em extended_diagnostic_results.json")

if __name__ == "__main__":
    main()

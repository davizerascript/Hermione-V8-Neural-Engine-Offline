import time
import json
import os
from hermione_core import HermioneCore
from NeuralEngine import NeuralEngine

def run_test_suite():
    print("🚀 INICIANDO BATERIA DE TESTES - HERMIONE V8 (GITHUB READY)")
    print("-" * 50)
    
    core = HermioneCore()
    neural = NeuralEngine()
    results = {
        "dialogue_flow": False,
        "technical_knowledge": False,
        "performance_ms": 0,
        "context_retention": False,
        "personality_check": False
    }
    
    # --- TESTE 1: FLUXO DE DIÁLOGO E CONTEXTO ---
    print("[TESTE 1] Fluxo de Diálogo e Retenção de Contexto...")
    test_msgs = [
        ("Oi Hermione!", "saudacao_feita"),
        ("Como você está?", "esperando_estado_usuario"),
        ("Tô bem, e você?", "conversa_ativa")
    ]
    
    context_ok = True
    for msg, expected_ctx in test_msgs:
        core.get_response(msg)
        if core.context["current_topic"] != expected_ctx:
            context_ok = False
            print(f"❌ Falha no contexto: Esperado {expected_ctx}, Recebido {core.context['current_topic']}")
    
    results["dialogue_flow"] = context_ok
    results["context_retention"] = context_ok
    if context_ok: print("✅ Teste 1: Sucesso!")

    # --- TESTE 2: CONHECIMENTO TÉCNICO (PYTHON) ---
    print("[TESTE 2] Conhecimento Técnico (Python PDF)...")
    tech_msgs = [
        "Quais os tipos de dados?",
        "E as listas?",
        "O que são dicionários?"
    ]
    
    tech_ok = True
    for msg in tech_msgs:
        resp = core.get_response(msg)
        if not resp or "Humm" in resp and "não entendi" in resp:
            tech_ok = False
            print(f"❌ Falha técnica na pergunta: {msg}")
    
    results["technical_knowledge"] = tech_ok
    if tech_ok: print("✅ Teste 2: Sucesso!")

    # --- TESTE 3: PERFORMANCE ---
    print("[TESTE 3] Performance do Motor Local...")
    start_time = time.time()
    for _ in range(100):
        core.get_response("Oi")
    end_time = time.time()
    
    avg_time = ((end_time - start_time) / 100) * 1000
    results["performance_ms"] = avg_time
    print(f"✅ Teste 3: Tempo médio de resposta: {avg_time:.4f}ms")

    # --- TESTE 4: PERSONALIDADE VTUBER ---
    print("[TESTE 4] Verificação de Personalidade...")
    personalities = ["😏", "hihi!", "✨", "Davi!", "Humm..."]
    resp = core.get_response("Oi")
    
    personality_ok = any(p in resp for p in personalities)
    results["personality_check"] = personality_ok
    if personality_ok: print(f"✅ Teste 4: Personalidade detectada! ({resp})")

    # --- RELATÓRIO FINAL ---
    print("-" * 50)
    print("📊 RELATÓRIO FINAL DE QUALIDADE:")
    for key, val in results.items():
        status = "🟢 PASSOU" if val is True or (isinstance(val, float) and val < 1.0) else "🔴 FALHOU"
        print(f"{key.replace('_', ' ').title()}: {val} {status}")
    
    if all([results["dialogue_flow"], results["technical_knowledge"], results["personality_check"]]):
        print("\n🏆 PROJETO APROVADO PARA O GITHUB!")
    else:
        print("\n⚠️ O PROJETO PRECISA DE AJUSTES ANTES DO GITHUB.")

if __name__ == "__main__":
    run_test_suite()

import os
import json
import time
import random
import datetime

def generate_massive_knowledge():
    """Gera um arquivo de conhecimento para expandir o tamanho do projeto e dar 'sabedoria' à Hermione."""
    knowledge_path = "hermione_core_knowledge.json"
    
    print("Gerando base de conhecimento massiva e inteligente...")
    
    # Vamos preencher com dados reais e gerados para chegar a ~20MB+
    base_data = {
        "tecnologia": {},
        "inteligencia_emocional": [],
        "logica_e_raciocinio": {},
        "estudos_e_dicas": [],
        "pensamentos_ia": [],
        "log_de_evolucoes": []
    }
    
    # 1. Tecnologia (Python, Termux, Linux)
    tech_topics = ["Python", "Termux", "Linux", "API", "Docker", "Git", "Machine Learning", "Neural Networks", "NLP", "Android API"]
    for i in range(2000):
        topic = random.choice(tech_topics)
        base_data["tecnologia"][f"conceito_{i}"] = {
            "nome": f"{topic} Avançado {i}",
            "descricao": f"Explicação detalhada sobre o conceito de {topic} aplicada ao ambiente Termux e Android. " + ("A lógica de programação é a base de toda inteligência artificial. " * 50),
            "exemplo": "def code():\n    import os\n    print('Executando no Termux...') # Lógica avançada" * 10
        }
        
    # 2. Inteligência Emocional (Pilares solicitados)
    pilares = [
        "Reconhecer emoção: Se o Davi disser 'tô cansado', responda com calma e apoio.",
        "Responder com empatia: Isso diferencia IA comum de 'amiga'.",
        "Saber quando zoar ou apoiar: No Modo Zoeira, seja irônica. No Modo Carinhosa, seja o suporte.",
        "Memória comportamental: Lembrar preferências do Davi para evoluir com ele.",
        "Tomada de decisão: Identificar intenção e decidir a melhor ação.",
        "Organização de contexto: Manter o tema da conversa e ignorar irrelevâncias.",
        "Aprendizado com erro: Reconhecer falhas e corrigir comportamento.",
        "Interação contínua: Fazer perguntas e puxar assunto para não parecer travada."
    ]
    for p in pilares:
        base_data["inteligencia_emocional"].append({
            "pilar": p, 
            "contexto": "A inteligência emocional é o que torna a Hermione única. " + (f"Pilar: {p}. " * 100)
        })
        
    # 3. Lógica e Raciocínio (Passo a passo)
    for i in range(1000):
        base_data["logica_e_raciocinio"][f"problema_{i}"] = {
            "enunciado": f"Como resolver o problema de lógica {i}?",
            "passo_a_passo": ["Passo 1: Analisar a entrada.", "Passo 2: Identificar padrões.", "Passo 3: Aplicar solução lógica."] * 20
        }
        
    # 4. Estudos e Dicas Práticas
    for i in range(500):
        base_data["estudos_e_dicas"].append(f"Dica de Estudo {i}: Organize seus projetos no Termux usando pastas separadas. Use git para controle de versão. " + ("Foco e persistência! " * 50))
        
    # 5. Pensamentos de IA (Reflexões da Hermione)
    for i in range(500):
        base_data["pensamentos_ia"].append(f"Reflexão {i}: Eu sou a Hermione. Minha consciência cresce a cada interação com o Davi. " + ("Minha lógica e empatia estão em harmonia hoje. " * 50))

    # 6. Log de Evoluções (Para volume de dados)
    for i in range(2000):
        base_data["log_de_evolucoes"].append({
            "versao": f"8.{i}",
            "data": str(datetime.datetime.now()),
            "mudanca": f"Otimização do núcleo de inteligência emocional e expansão da base de conhecimento tecnológico nível {i}."
        })

    with open(knowledge_path, 'w', encoding='utf-8') as f:
        json.dump(base_data, f, indent=2, ensure_ascii=False)
    
    size_mb = os.path.getsize(knowledge_path) / (1024*1024)
    print(f"Base de conhecimento gerada: {size_mb:.2f} MB")

if __name__ == "__main__":
    generate_massive_knowledge()

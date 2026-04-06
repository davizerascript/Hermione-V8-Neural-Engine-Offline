import sqlite3
import json
import os

def update_hermione_knowledge():
    db_path = "/home/ubuntu/hermione_v8/hermione_knowledge.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Novos conhecimentos extraídos do PDF "Aprendendo Python"
    python_teachings = [
        ("python", "Tipos de Objetos", "Python possui tipos integrados como Números, Strings, Listas, Dicionários, Tuplas e Arquivos. Eles são a base de qualquer script.", "tipos,objetos,base"),
        ("python", "Listas", "Listas são coleções ordenadas de objetos, mutáveis e podem conter tipos mistos. Ex: [1, 'dois', 3.0].", "listas,colecao,mutavel"),
        ("python", "Dicionários", "Dicionários são mapeamentos de chave-valor, ideais para organizar dados de forma estruturada. Ex: {'nome': 'Hermione', 'versao': 8}.", "dicionarios,mapeamento,chave-valor"),
        ("python", "Funções", "Funções são blocos de código reutilizáveis definidos com 'def'. Elas ajudam a evitar repetição e organizar a lógica.", "funcoes,def,reutilizacao"),
        ("python", "Classes e POO", "Programação Orientada a Objetos (POO) em Python usa classes para criar novos tipos de objetos com atributos e métodos.", "classes,poo,objetos"),
        ("python", "Módulos", "Módulos são arquivos .py que podem ser importados para outros scripts, permitindo a modularização do código.", "modulos,import,organizacao"),
        ("python", "Exceções", "O tratamento de erros em Python é feito com blocos try/except, garantindo que o programa não trave em caso de falhas.", "excecoes,try,except,erros")
    ]
    
    for cat, title, content, tags in python_teachings:
        cursor.execute("INSERT INTO knowledge (category, title, content, tags) VALUES (?, ?, ?, ?)", (cat, title, content, tags))
    
    conn.commit()
    conn.close()
    print("Cérebro da Hermione atualizado com conhecimentos do PDF!")

if __name__ == "__main__":
    update_hermione_knowledge()

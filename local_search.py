import sqlite3
import os

DB_PATH = "hermione_knowledge.db"

def search_local(query, limit=3):
    """Busca na base de conhecimento local usando FTS5."""
    if not os.path.exists(DB_PATH):
        return "Base de conhecimento local não encontrada."
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Correção definitiva: FTS5 não gosta de aliases em tabelas virtuais em algumas versões do SQLite
        # Vamos usar os nomes completos das tabelas para garantir compatibilidade total no Termux
        cursor.execute("""
            SELECT knowledge.title, knowledge.content, knowledge.category 
            FROM knowledge
            JOIN knowledge_idx ON knowledge.id = knowledge_idx.rowid
            WHERE knowledge_idx MATCH ? 
            ORDER BY rank 
            LIMIT ?
        """, (query, limit))
        
        results = cursor.fetchall()
        conn.close()
        
        if not results:
            return f"Não encontrei nada local sobre '{query}', Davi."
        
        formatted_results = []
        for title, content, category in results:
            # Limpar o conteúdo de repetições se houver (devido à expansão massiva)
            clean_content = content[:500]
            formatted_results.append(f"[{category.upper()}] {title}: {clean_content}...")
            
        return "\n\n".join(formatted_results)
    except Exception as e:
        return f"Erro na busca local: {str(e)}"

if __name__ == "__main__":
    # Teste rápido
    print(search_local("python"))
    print("-" * 20)
    print(search_local("termux"))

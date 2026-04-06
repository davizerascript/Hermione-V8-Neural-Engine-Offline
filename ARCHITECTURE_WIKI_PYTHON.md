# Arquitetura da Base de Conhecimento Hermione V8 (Termux Optimized)

## 1. Objetivos
- Integrar resumos da Wikipedia (PT-BR) localmente.
- Integrar documentação avançada de Python e exemplos de scripts.
- Manter o tamanho total abaixo de 1GB (idealmente ~500MB para folga).
- Sistema de busca por palavra-chave ultra-rápido usando SQLite FTS5 (Full Text Search).

## 2. Estrutura de Dados (SQLite)
Usaremos um banco de dados SQLite (`hermione_knowledge.db`) com as seguintes tabelas:

### Tabela: `knowledge`
- `id`: INTEGER PRIMARY KEY
- `category`: TEXT (wiki, python, termux, logic)
- `title`: TEXT (Título do artigo ou conceito)
- `content`: TEXT (Conteúdo resumido/comprimido)
- `tags`: TEXT (Palavras-chave para busca rápida)

### Tabela Virtual (FTS5): `knowledge_idx`
- Para busca de texto completo em `title`, `content` e `tags`.

## 3. Estratégia de Compressão
- **Wikipedia:** Focar nos 50.000 artigos mais acessados em PT-BR (resumos).
- **Python:** Documentação oficial (PEP, Built-ins, Standard Library) + 1000+ snippets de código úteis.
- **Armazenamento:** O SQLite por si só é eficiente, mas usaremos `zlib` ou `lzma` para blocos de texto se necessário para atingir o limite de 1GB com mais dados.

## 4. Sistema de Busca
- Função `search_local(query)` que consulta o SQLite.
- Integração no `handle_tools` do `main.py` para interceptar perguntas e consultar a base local antes da API (ou para enriquecer o prompt).

## 5. Treinamento em Python
- Inclusão de um "Script Generator Handbook" na base de dados.
- Exemplos de automação Termux (API, SMS, Notificações, Sistema de Arquivos).
- Padrões de projeto (Clean Code, SOLID) adaptados para scripts rápidos.

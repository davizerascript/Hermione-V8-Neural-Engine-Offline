# Hermione Neural V8 - Guia de Instalação (Termux)

Davi, aqui estão as instruções para rodar a nova versão da Hermione com a base de conhecimento da Wikipedia e treinamento avançado em Python.

## 1. Requisitos no Termux
Certifique-se de ter o Python e o SQLite instalados:
```bash
pkg update && pkg upgrade
pkg install python sqlite termux-api mpv
pip install requests edge-tts
```

## 2. Como Iniciar
Basta rodar o script principal:
```bash
python main.py
```

## 3. Novidades desta Versão
- **Base de Conhecimento Local:** Agora a Hermione tem um banco de dados SQLite (`hermione_knowledge.db`) com resumos da Wikipedia e documentação de Python.
- **Busca por Palavra-Chave:** Ela busca automaticamente na base local antes de ir para a internet, economizando dados e sendo muito mais rápida.
- **Mestre em Python:** O cérebro dela foi ajustado para gerar scripts melhores, seguindo as melhores práticas de programação.
- **Otimização de Espaço:** Removemos os arquivos JSON gigantes e repetitivos, substituindo por um banco de dados eficiente que respeita o limite de 1GB.

## 4. Comandos Úteis
- `wiki [assunto]`: Busca na base local e na Wikipedia.
- `como faz [assunto]`: Busca tutoriais e documentação de Python.
- `limpar`: Limpa a memória da conversa atual.
- `sair`: Salva o estado mental da Hermione e fecha.

---
**Dica:** Se você quiser expandir a base de conhecimento ainda mais, pode rodar o `knowledge_builder.py`, mas cuidado para não passar do limite de armazenamento do seu celular!

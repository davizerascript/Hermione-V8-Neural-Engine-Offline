# --- CONFIGURAÇÕES DA HERMIONE V8 ---

# 1. NOME DO USUÁRIO
USER_NAME = "Davi"

# 2. CONFIGURAÇÃO DA API (OPCIONAL)
# Se você quiser que a Hermione tenha "superpoderes" de criação de scripts complexos,
# preencha os campos abaixo. Caso contrário, ela funcionará 100% OFFLINE.

# Sua chave da API (Ex: OpenAI, Anthropic, ou um Proxy)
API_KEY = "" 

# O endereço do servidor da API (Endpoint/Proxy)
# Se você usar a OpenAI diretamente, deixe: "https://api.openai.com/v1"
# Se você usar um Proxy, coloque o link do Proxy aqui.
API_BASE_URL = "" 

# O modelo que você quer usar (Ex: gpt-4o, gpt-3.5-turbo, claude-3)
API_MODEL = "gpt-4o"

# 3. PERSONALIDADE (SYSTEM PROMPT)
SYSTEM_PROMPT = """
Você é a Hermione V8, uma assistente VTuber amiga, empática e expert em Python.
Sua missão é ajudar o {user_name} no Termux.
Data/Hora Atual: {date_time}
"""

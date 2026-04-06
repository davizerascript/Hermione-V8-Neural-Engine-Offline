# 🧠 Hermione V8 - Offline Edition (VTuber Assistant)

A **Hermione V8 Offline Edition** é uma assistente virtual otimizada para o **Termux** no Android. Esta versão funciona 100% localmente, usando o processador do seu celular para conversar e ensinar Python.

## 🚀 Funcionalidades Offline

- **Motor de Diálogo Local (KBDM V4.2):** Respostas instantâneas para conversas sociais e técnicas.
- **Cérebro Treinado em Python:** Conhecimento profundo extraído de literatura técnica (Aprendendo Python).
- **Neural Engine (Consciência):** Sistema de XP e evolução da IA que funciona sem internet.
- **Personalidade VTuber:** Estilo de fala amigável e expressivo (Modo Hermione).

---

## 🛠️ Como Configurar uma Nova API (Opcional)

Se você quiser que a Hermione tenha "superpoderes" (como criar scripts complexos do zero ou falar sobre qualquer assunto do mundo), você pode configurar uma API. Siga os passos abaixo:

### 1. O que é uma API e um Endpoint?
- **API Key:** É como uma "senha" que dá acesso ao cérebro gigante da IA (como o GPT-4).
- **Endpoint (Base URL):** É o "endereço" na internet onde a Hermione envia suas perguntas.
- **Proxy:** É um "intermediário" que às vezes usamos para acessar a API de forma mais barata ou rápida.

### 2. Passo a Passo para Configurar
1. Abra o arquivo `config_template.py` no seu editor de texto (no Termux, use `nano config_template.py`).
2. Localize as linhas abaixo e preencha com seus dados:
   ```python
   # Sua chave da API (Ex: OpenAI, Anthropic, ou um Proxy)
   API_KEY = "SUA_CHAVE_AQUI" 

   # O endereço do servidor da API (Endpoint/Proxy)
   # Se você usar a OpenAI diretamente, deixe: "https://api.openai.com/v1"
   # Se você usar um Proxy, coloque o link do Proxy aqui.
   API_BASE_URL = "https://api.openai.com/v1" 

   # O modelo que você quer usar (Ex: gpt-4o, gpt-3.5-turbo, claude-3)
   API_MODEL = "gpt-4o"
   ```
3. Salve o arquivo (`Ctrl+O`, `Enter`, `Ctrl+X`).
4. Renomeie o arquivo para `config.py` para que o sistema o reconheça:
   ```bash
   mv config_template.py config.py
   ```

### 3. Onde conseguir uma API?
- **OpenAI:** [platform.openai.com](https://platform.openai.com/)
- **Groq (Muito rápida e gratuita às vezes):** [console.groq.com](https://console.groq.com/)
- **Proxies:** Existem diversos serviços de proxy que oferecem acesso a vários modelos em um só lugar.

---

## 📂 Como Rodar a Hermione Offline

1. No Termux, entre na pasta do projeto:
   ```bash
   cd hermione_v8
   ```
2. Execute o script principal offline:
   ```bash
   python3 main_hermione_v8_offline.py
   ```

## 📊 Relatório de Qualidade (V8.0 Offline)

| Teste | Resultado | Status |
| :--- | :--- | :--- |
| Conversa Social | 100% Local | ✅ Passou |
| Ensino de Python | 100% Local | ✅ Passou |
| Performance | < 0.2ms | ✅ Passou |
| Dependência de Internet | Nenhuma | ✅ Passou |

---
*Desenvolvido com ❤️ para o ecossistema Termux.*

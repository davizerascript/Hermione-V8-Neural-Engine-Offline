import requests
import json
import config

def get_hermione_response(messages):
    """
    Obtém a resposta da Hermione usando a biblioteca requests.
    Ideal para ambientes como Termux onde a biblioteca openai pode ser difícil de instalar.
    """
    # O proxy do Manus espera o endpoint completo de chat completions
    url = f"{config.BASE_URL}/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {config.API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": config.MODEL,
        "messages": messages
    }
    
    try:
        # Timeout de 30 segundos para evitar travamentos no Termux
        response = requests.post(url, headers=headers, data=json.dumps(payload), timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            return data['choices'][0]['message']['content']
        else:
            # Tratamento de erros amigável no estilo Hermione
            error_msg = f"Poxa Davi, deu um erro {response.status_code} aqui na minha cabeça. Tenta de novo?"
            try:
                # Tenta extrair mensagem de erro detalhada se disponível
                detail = response.json().get('error', {}).get('message', '')
                if detail:
                    print(f"\033[1;31m[DEBUG: {detail}]\033[0m")
            except:
                pass
            return error_msg
            
    except requests.exceptions.Timeout:
        return "Davi, a internet tá uma carroça, amigo. Deu timeout aqui."
    except Exception as e:
        return f"Davi, tá rolando um erro estranho aqui: {str(e)}"

import requests
import json

def search_wikipedia(query):
    """Busca um resumo na Wikipedia."""
    url = "https://pt.wikipedia.org/api/rest_v1/page/summary/" + query.replace(" ", "_")
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return f"Resumo Wiki ({query}): {data.get('extract', 'Não achei detalhes.')}"
        return f"Não achei nada sobre '{query}' na Wiki, Davi."
    except:
        return "Erro ao acessar a Wiki."

def search_web(query):
    """Simula uma busca web via DuckDuckGo."""
    url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            abstract = data.get('AbstractText', '')
            return f"Web: {abstract}" if abstract else "Busca sem resumo direto."
        return "Internet tá de sacanagem, não consegui buscar."
    except:
        return "Erro na busca web."

def get_crypto_price(coin="bitcoin"):
    """Pega o preço de criptomoedas via CoinGecko."""
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin.lower()}&vs_currencies=usd,brl"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if coin.lower() in data:
                usd = data[coin.lower()]['usd']
                brl = data[coin.lower()]['brl']
                return f"Cripto ({coin}): ${usd} | R${brl}"
        return f"Não achei o preço de {coin}, gênio."
    except:
        return "Erro ao pegar cotação cripto."

def get_weather(city="São Paulo"):
    """Pega o clima via wttr.in (API simples e gratuita)."""
    url = f"https://wttr.in/{city}?format=3"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return f"Clima: {response.text.strip()}"
        return f"Não achei o clima de {city}."
    except:
        return "Erro ao checar o tempo."

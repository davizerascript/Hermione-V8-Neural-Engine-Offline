import subprocess
import os
import urllib.parse

def run_termux_command(command):
    """Executa um comando do Termux e retorna a saída."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip() if result.returncode == 0 else None
    except:
        return None

def open_app(app_name):
    """Tenta abrir um aplicativo no Android via Termux."""
    app_name = app_name.lower()
    
    # Mapeamento de nomes comuns para intents ou pacotes
    apps = {
        "youtube": "am start -a android.intent.action.VIEW -d https://www.youtube.com",
        "whatsapp": "am start -n com.whatsapp/.Main",
        "instagram": "am start -n com.instagram.android/com.instagram.main.activity.MainActivity",
        "spotify": "am start -n com.spotify.music/com.spotify.music.MainActivity",
        "navegador": "am start -a android.intent.action.VIEW -d https://www.google.com",
        "chrome": "am start -n com.android.chrome/com.google.android.apps.chrome.Main",
        "calculadora": "am start -n com.google.android.calculator/com.android.calculator2.Calculator",
        "calendario": "am start -n com.google.android.calendar/com.android.calendar.AllInOneActivity",
        "configurações": "am start -a android.settings.SETTINGS",
        "wifi": "am start -a android.settings.WIFI_SETTINGS",
        "bluetooth": "am start -a android.settings.BLUETOOTH_SETTINGS"
    }
    
    if app_name in apps:
        run_termux_command(apps[app_name])
        return f"Abrindo {app_name.capitalize()} agora mesmo, Davi! 😉"
    
    # Se não estiver no mapa, tenta uma busca genérica ou avisa
    return f"Ainda não sei abrir o '{app_name}' diretamente, mas posso tentar aprender se você me ensinar o comando! 😅"

def search_youtube(query):
    """Pesquisa um vídeo no YouTube."""
    encoded_query = urllib.parse.quote(query)
    url = f"https://www.youtube.com/results?search_query={encoded_query}"
    run_termux_command(f"am start -a android.intent.action.VIEW -d \"{url}\"")
    return f"Pesquisando '{query}' no YouTube pra você! 📺"

def make_call(number):
    """Inicia uma chamada telefônica."""
    run_termux_command(f"am start -a android.intent.action.CALL -d tel:{number}")
    return f"Ligando para {number}... 📞"

def send_sms(number, message):
    """Envia um SMS."""
    run_termux_command(f"termux-sms-send -n {number} \"{message}\"")
    return f"SMS enviado para {number}! ✉️"

def get_battery_status():
    """Retorna o status da bateria via Termux API."""
    status = run_termux_command("termux-battery-status")
    if status:
        import json
        data = json.loads(status)
        return f"Sua bateria está em {data['percentage']}% e o status é {data['status']}. 🔋"
    return "Não consegui ver a bateria agora. Você instalou o Termux:API? 🤔"

def set_brightness(level):
    """Define o brilho da tela (0-255)."""
    run_termux_command(f"termux-brightness {level}")
    return f"Brilho ajustado para {level}! 💡"

def vibrate(duration=500):
    """Faz o celular vibrar."""
    run_termux_command(f"termux-vibrate -d {duration}")
    return "Bzzzz! Sentiu aí? 😂"

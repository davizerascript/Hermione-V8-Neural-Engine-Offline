import os
import subprocess
import asyncio
import edge_tts
import time

# Configurações de Voz VTuber
# Thalita é a voz feminina brasileira mais expressiva para esse estilo.
VOICE = "pt-BR-ThalitaMultilingualNeural"
TEMP_AUDIO_FILE = "response.mp3"

def analyze_emotion(text):
    """Analisa o texto para ajustar a velocidade e o tom da voz."""
    text = text.lower()
    rate = "+10%"  # Padrão: Um pouco mais rápido para parecer animada
    pitch = "+5Hz" # Padrão: Um pouco mais agudo para estilo anime
    
    # Se estiver animada ou brava, fala mais rápido
    if any(x in text for x in ["feliz", "oba", "legal", "nao", "para", "erro", "brava"]):
        rate = "+25%"
        pitch = "+10Hz"
    # Se estiver pensativa ou triste, fala mais devagar e grave
    elif any(x in text for x in ["humm", "acho", "talvez", "triste", "pena", "infelizmente"]):
        rate = "-5%"
        pitch = "-2Hz"
    # Se estiver sendo fofa/carinhosa
    elif any(x in text for x in ["linda", "fofa", "gosto", "amiga", "obrigada"]):
        rate = "+5%"
        pitch = "+15Hz" # Mais agudo estilo anime
        
    return rate, pitch

async def generate_speech(text, output_file=TEMP_AUDIO_FILE):
    """Gera um arquivo de áudio a partir do texto usando Edge TTS."""
    rate, pitch = analyze_emotion(text)
    communicate = edge_tts.Communicate(text, VOICE, rate=rate, pitch=pitch)
    await communicate.save(output_file)

def play_audio(file_path=TEMP_AUDIO_FILE):
    """Reproduz o áudio no Termux usando o comando play-audio ou mpv."""
    if os.path.exists(file_path):
        try:
            # Silencia as saídas dos comandos para não sujar o terminal
            subprocess.run(["play-audio", file_path], check=True, capture_output=True)
        except:
            try:
                subprocess.run(["mpv", "--no-video", file_path], check=True, capture_output=True)
            except:
                pass # Se falhar, apenas continua sem áudio

def listen_voice():
    """Captura voz do usuário usando termux-speech-to-text."""
    print(f"\n\033[1;33m(Ouvindo...)\033[0m")
    try:
        result = subprocess.run(["termux-speech-to-text"], capture_output=True, text=True)
        if result.returncode == 0:
            text = result.stdout.strip()
            if text:
                print(f"\033[1;32mVocê (Voz):\033[0m {text}")
                return text
        return None
    except Exception as e:
        print(f"\n[Erro no STT: Certifique-se de que o termux-api está instalado e as permissões de microfone concedidas.]")
        return None

def speak(text):
    """Função síncrona para facilitar o uso no loop principal."""
    if not text: return
    try:
        asyncio.run(generate_speech(text))
        play_audio()
    except Exception as e:
        pass # Falha silenciosa para não quebrar o loop

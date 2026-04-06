import subprocess
import os
import base64
import requests
import json
import config

# Configurações de Visão
TEMP_IMAGE_PATH = "hermione_eyes.jpg"

def take_photo():
    """Tira uma foto usando a câmera do Termux (necessário termux-api)."""
    print(f"\n\033[1;33m(Hermione abrindo os olhos...)\033[0m")
    try:
        # Tenta tirar foto com a câmera traseira (0) ou frontal (1)
        # Usamos termux-camera-photo para capturar a imagem
        subprocess.run(["termux-camera-photo", "-c", "1", TEMP_IMAGE_PATH], check=True, capture_output=True)
        if os.path.exists(TEMP_IMAGE_PATH):
            return TEMP_IMAGE_PATH
        return None
    except Exception as e:
        print(f"\n[Erro na Câmera: Certifique-se de que o termux-api está instalado e a permissão de câmera concedida.]")
        return None

def encode_image(image_path):
    """Codifica a imagem em base64 para enviar para a API."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def analyze_image(image_path, prompt="O que você está vendo nesta imagem? Seja breve e fale como a Hermione."):
    """Envia a imagem para a API de visão do Manus/OpenAI."""
    if not os.path.exists(image_path):
        return "Não consegui ver nada, Davi. A câmera falhou."

    base64_image = encode_image(image_path)
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.API_KEY}"
    }

    payload = {
        "model": "gpt-4o-mini", # Usamos o mini-vision para ser rápido
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    try:
        response = requests.post(config.BASE_URL + "/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        return f"Houve um erro ao processar a imagem: {str(e)}"
    finally:
        # Limpa a imagem temporária após o uso
        if os.path.exists(image_path):
            os.remove(image_path)

def see_and_comment(prompt="Comente o que você vê de forma amigável."):
    """Função completa: Tira foto e analisa."""
    img = take_photo()
    if img:
        return analyze_image(img, prompt)
    return "Não consegui abrir meus olhos agora, Davi. Algo deu errado com a câmera."

#!/bin/bash

echo "Instalando dependências para voz na Hermione..."

# Atualizar pacotes
pkg update && pkg upgrade -y

# Instalar Termux API (Necessário para STT e áudio)
pkg install termux-api -y

# Instalar MPV para reprodução de áudio
pkg install mpv -y

# Instalar dependências Python
pip install edge-tts

echo "---------------------------------------------------"
echo "IMPORTANTE:"
echo "1. Certifique-se de ter o app 'Termux:API' instalado da Play Store ou F-Droid."
echo "2. Conceda permissão de microfone ao Termux."
echo "3. Para falar, basta dar ENTER sem digitar nada no chat."
echo "---------------------------------------------------"
echo "Instalação concluída! Agora você pode rodar: python main.py"

import random

# Biblioteca de Expressões Faciais VTuber ASCII
EXPRESSIONS = {
    "HAPPY": "(◕‿◕✿)  -  Oii Davi-kun!",
    "THINKING": "(。-`ω´-)  -  Humm... deixa eu pensar...",
    "ANGRY": "ヽ( `д´*)ノ  -  Peraí, você tá falando sério?!",
    "SURPRISED": "(⊙_⊙)  -  Nossa! Não esperava por essa!",
    "SHY": "(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)  -  Ai, assim você me deixa sem jeito...",
    "SAD": "(╥﹏╥)  -  Poxa... que chato isso.",
    "COOL": "(⌐■_■)  -  Tudo sob controle, Davi.",
    "SMILE": "(^人^)  -  Hehehe!",
    "WINK": "(^_-)  -  Pode deixar comigo!",
    "IDLE": "(´｡• ᵕ •｡`)  -  Tô por aqui..."
}

def get_expression(text):
    """Detecta qual expressão ASCII usar com base no texto da resposta."""
    text = text.lower()
    if any(x in text for x in ["feliz", "bom", "legal", "obrigado", "boa", "oi", "ola"]):
        return EXPRESSIONS["HAPPY"]
    if any(x in text for x in ["pensando", "talvez", "acho", "hum", "duvida"]):
        return EXPRESSIONS["THINKING"]
    if any(x in text for x in ["brava", "irritada", "nao", "pare", "erro"]):
        return EXPRESSIONS["ANGRY"]
    if any(x in text for x in ["nossa", "serio", "caramba", "uau"]):
        return EXPRESSIONS["SURPRISED"]
    if any(x in text for x in ["linda", "fofa", "gosto", "amiga"]):
        return EXPRESSIONS["SHY"]
    if any(x in text for x in ["triste", "pena", "infelizmente", "perdao"]):
        return EXPRESSIONS["SAD"]
    if any(x in text for x in ["consegui", "pronto", "facil", "resolvido"]):
        return EXPRESSIONS["COOL"]
    
    return EXPRESSIONS["IDLE"]

def show_vtuber(text):
    """Exibe a face da Hermione no terminal."""
    face = get_expression(text)
    print("\n" + "="*40)
    print(f"\033[1;35m      {face}\033[0m")
    print("="*40 + "\n")

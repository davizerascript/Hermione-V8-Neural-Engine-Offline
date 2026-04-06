import os
from openai import OpenAI

client = OpenAI()

try:
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": "Oi"}]
    )
    print("Sucesso!")
    print(response.choices[0].message.content)
except Exception as e:
    print(f"Erro: {e}")

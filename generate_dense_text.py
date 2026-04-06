import random
import string

def generate_dense_text(filename, size_mb):
    """Gera um arquivo de texto com palavras reais e aleatórias para evitar compressão de 100%."""
    words = ["Python", "Termux", "Linux", "IA", "Hermione", "Lógica", "Código", "Davi", "Desenvolvimento", "Terminal", "API", "Neural", "Consciência", "Empatia", "Estudo"]
    print(f"Gerando {size_mb}MB de texto denso e útil...")
    with open(filename, 'w', encoding='utf-8') as f:
        for _ in range(size_mb * 10000): # Aproximadamente 100 bytes por iteração
            line = " ".join(random.choices(words, k=10)) + " " + "".join(random.choices(string.ascii_letters, k=20)) + "\n"
            f.write(line)
    print("Concluído.")

if __name__ == "__main__":
    generate_dense_text("CONHECIMENTO_NEURAL_DENSO.txt", 90)

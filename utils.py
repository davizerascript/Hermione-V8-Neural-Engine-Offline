import os
import subprocess

def check_dependencies():
    """Verifica se as dependências básicas estão instaladas."""
    try:
        import requests
        return True
    except ImportError:
        print("Erro: A biblioteca 'requests' não foi encontrada.")
        print("Instale-a com: pip install requests")
        return False

def create_startup_script():
    """Cria um script shell simples para iniciar a Hermione mais fácil."""
    script_content = "#!/bin/bash\npython3 main.py"
    with open("hermione.sh", "w") as f:
        f.write(script_content)
    os.chmod("hermione.sh", 0o755)
    return "Script 'hermione.sh' criado com sucesso."

def setup_project():
    """Configuração inicial do projeto."""
    print("Configurando Hermione V3...")
    check_dependencies()
    create_startup_script()
    print("Tudo pronto, Davi. Só rodar 'bash hermione.sh'!")

if __name__ == "__main__":
    setup_project()

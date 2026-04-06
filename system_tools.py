import subprocess
import os

def run_command(command):
    """Executa um comando no shell e retorna a saída."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return f"Erro na execução: {result.stderr.strip()}"
    except Exception as e:
        return f"Falha catastrófica: {str(e)}"

def get_system_info():
    """Retorna informações básicas do sistema Termux."""
    return {
        "uptime": run_command("uptime"),
        "whoami": run_command("whoami"),
        "pwd": os.getcwd(),
        "files": run_command("ls -F")
    }

def list_packages():
    """Lista pacotes instalados no Termux via pkg."""
    return run_command("pkg list-installed")

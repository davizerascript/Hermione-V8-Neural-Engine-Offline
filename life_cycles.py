import datetime
import os
import json

DIARY_FILE = "hermione_diary.json"

def get_time_context():
    """Retorna o contexto temporal para o prompt da Hermione."""
    now = datetime.datetime.now()
    hour = now.hour
    
    if 5 <= hour < 12:
        period = "Manhã"
        greeting = "Bom dia"
    elif 12 <= hour < 18:
        period = "Tarde"
        greeting = "Boa tarde"
    elif 18 <= hour < 23:
        period = "Noite"
        greeting = "Boa noite"
    else:
        period = "Madrugada"
        greeting = "Madrugada"
        
    return {
        "full_date": now.strftime("%d/%m/%Y"),
        "time": now.strftime("%H:%M"),
        "period": period,
        "greeting": greeting,
        "is_late": hour >= 23 or hour < 5
    }

def save_to_diary(user_input, assistant_response):
    """Salva um resumo da interação no diário episódico."""
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    
    diary = {}
    if os.path.exists(DIARY_FILE):
        try:
            with open(DIARY_FILE, 'r', encoding='utf-8') as f:
                diary = json.load(f)
        except:
            diary = {}
            
    if date_str not in diary:
        diary[date_str] = []
        
    entry = {
        "time": now.strftime("%H:%M"),
        "user": user_input[:100], # Limita tamanho
        "hermione": assistant_response[:100]
    }
    
    diary[date_str].append(entry)
    
    # Manter apenas os últimos 30 dias
    if len(diary) > 30:
        oldest_date = sorted(diary.keys())[0]
        del diary[oldest_date]
        
    with open(DIARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(diary, f, indent=4, ensure_ascii=False)

def get_diary_summary():
    """Retorna um resumo das últimas entradas do diário."""
    if not os.path.exists(DIARY_FILE):
        return "Nenhum registro no diário ainda."
        
    try:
        with open(DIARY_FILE, 'r', encoding='utf-8') as f:
            diary = json.load(f)
            
        dates = sorted(diary.keys(), reverse=True)
        if not dates:
            return "Diário vazio."
            
        last_date = dates[0]
        entries = diary[last_date][-3:] # Últimas 3 entradas do dia mais recente
        
        summary = f"No dia {last_date}, conversamos sobre:\n"
        for e in entries:
            summary += f"- Às {e['time']}: {e['user']}\n"
        return summary
    except:
        return "Erro ao ler o diário."

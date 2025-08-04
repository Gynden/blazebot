import time
import requests
import telegram
from datetime import datetime, timedelta

TOKEN = '8144201595:AAFg4j7TM1ChTzopBbrJyXG-8xv3APDgOcw'
GROUP_ID = -4890083404
bot = telegram.Bot(token=TOKEN)

# Histórico de padrões que resultaram em branco
memory = []

# Último timeout por WIN
last_win_time = None

# Captura resultados dos últimos ~100 giros
def get_results():
    try:
        resp = requests.get("https://blaze-1.com/api/roulette_games/recent?limit=100")
        arr = [r["color"] for r in resp.json()]
        return arr
    except: return []

def analyze(res):
    steps = []
    points = 0
    now = datetime.utcnow()

    # Giros sem branco
    no_white = next((i for i, c in enumerate(res) if c == 0), len(res))
    if no_white >= 13:
        points += 1
        steps.append("13+ sem branco")

    # Sequência de mesma cor
    seq = 1
    for i in range(1, len(res)):
        if res[i] == res[i-1] and res[i] != 0:
            seq += 1
        else: break
    if seq >= 5:
        points += 1
        steps.append(f"{seq} da mesma cor")

    # Alternância
    alt = sum(1 for i in range(2, len(res)) if res[i] != res[i-2])
    if alt >= 6:
        points += 1
        steps.append("Alternância intensa")

    # Tempo desde último branco
    # Supondo timestamps se existirem, ou por índice estimado ~30s por giro
    if no_white * 30 >= 13 * 60:
        points += 1
        steps.append("≥13 min sem branco")

    # Reentrada após branco
    if res and res[0] == 1:  # se o último foi branco
        points += 1
        steps.append("Reentrada recente")

    # Padrão recorrente
    key = (no_white, seq, alt)
    if key in memory:
        points += 2
        steps.append("Padrão recorrente detectado")

    return points, steps, key

def send_signal(pts, steps):
    global last_win_time
    msg = "🚨 ENTRADA RECOMENDADA NO BRANCO\n\n"
    msg += "📊 Condições:\n" + "".join(f"✅ {s}\n" for s in steps)
    msg += "\n🎯 R$2 no branco – Martingale até 4x – Válido por 5 giros"
    bot.send_message(chat_id=GROUP_ID, text=msg)
    return datetime.utcnow()

def track_outcome(old_len):
    res = get_results()
    for i in range(min(5, len(res))):
        if res[i] == 0:
            bot.send_message(chat_id=GROUP_ID, text=f"✅ GREEN no giro {i+1} após sinal!")
            return True
    bot.send_message(chat_id=GROUP_ID, text="❌ STOP – branco não saiu nos 5 giros.")
    return False

def main():
    global last_win_time
    already_signaled = False
    while True:
        res = get_results()
        if not res:
            time.sleep(15)
            continue
        if last_win_time and datetime.utcnow() - last_win_time < timedelta(minutes=30):
            time.sleep(15)
            continue

        pts, steps, key = analyze(res)
        if pts >= 3 and not already_signaled:
            last_win_time = send_signal(pts, steps)
            already_signaled = True
            memory.append(key)
            # verificar o resultado após 5 giros
            time.sleep(30)
            track_outcome(len(res))
        elif pts < 3:
            already_signaled = False

        time.sleep(15)

if __name__ == "__main__":
    main()

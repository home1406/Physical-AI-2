import sqlite3, time, requests
 
TELEGRAM_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
THRESHOLDS = {"temp": (0, 35), "hum": (10, 90), "dist": (5, None)}
 
def notify(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        requests.post(url, json={"chat_id": CHAT_ID, "text": message}, timeout=5)
    except requests.RequestException as e:
        print("알림 전송 실패:", e)
 
def check_thresholds(reading, last_alert):
    now = time.time()
    for key, (lo, hi) in THRESHOLDS.items():
        value = reading.get(key)
        if value is None:
            continue
        out_of_range = (lo is not None and value < lo) or (hi is not None and value > hi)
        cooldown_ok = now - last_alert.get(key, 0) > 300  # 5분 쿨다운
        if out_of_range and cooldown_ok:
            notify(f"경고: {key}={value} (허용범위 {lo}~{hi} 벗어남)")
            last_alert[key] = now
 
conn = sqlite3.connect("sensors.db")
last_alert = {}
print("임계값 모니터링 시작")
while True:
    cur = conn.execute(
        "SELECT temp, hum, dist FROM readings ORDER BY id DESC LIMIT 1")
    row = cur.fetchone()
    if row:
        reading = {"temp": row[0], "hum": row[1], "dist": row[2]}
        check_thresholds(reading, last_alert)
    time.sleep(10)

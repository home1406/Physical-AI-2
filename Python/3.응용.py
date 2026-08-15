import sqlite3, time, threading
from datetime import datetime
 
DB_PATH = "sensors.db"
 
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ts TEXT NOT NULL,
        temp REAL, hum REAL, dist REAL, pir INTEGER
    )""")
    conn.commit()
    return conn
 
shared = {"temp": None, "hum": None, "dist": None, "pir": 0}
lock = threading.Lock()
 
def logger_loop(conn, interval=5.0):
    while True:
        with lock:
            row = dict(shared)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        conn.execute(
            "INSERT INTO readings (ts, temp, hum, dist, pir) VALUES (?,?,?,?,?)",
            (now, row["temp"], row["hum"], row["dist"], row["pir"]),
        )
        conn.commit()
        time.sleep(interval)
 
if __name__ == "__main__":
    conn = init_db()
    threading.Thread(target=logger_loop, args=(conn,), daemon=True).start()
    print("통합 로거 시작 — 센서 읽기 스레드에서 shared 딕셔너리를 갱신하세요")
    while True:
        time.sleep(1)

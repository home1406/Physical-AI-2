# ── 라즈베리파이 Python 코드 ────────────────────────────
# pip install pyserial
import serial, json, time, csv
from datetime import datetime

# ls /dev/ttyUSB*  또는  ls /dev/ttyACM* 으로 포트 확인
PORT = "/dev/ttyUSB0"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=1)
time.sleep(2)   # 아두이노 리셋 완료 대기 (필수!)

# 아두이노 "READY" 메시지 대기
while True:
    line = ser.readline().decode("utf-8", errors="ignore").strip()
    if line == "READY":
        print("아두이노 준비 완료!")
        break

# CSV 파일 준비
with open("sensor_log.csv", "w", newline="") as f:
    csv.writer(f).writerow(["timestamp", "temperature", "humidity"])

try:
    while True:
        if ser.in_waiting > 0:
            raw = ser.readline().decode("utf-8", errors="ignore").strip()
            if not raw.startswith("{"):
                continue
            try:
                data = json.loads(raw)
                temp = data["temp"]
                hum  = data["hum"]
                now  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"[{now}]  {temp:.1f}°C  {hum:.1f}%")
                with open("sensor_log.csv", "a", newline="") as f:
                    csv.writer(f).writerow([now, temp, hum])
            except (json.JSONDecodeError, KeyError) as e:
                print(f"파싱 오류: {e}")
        time.sleep(0.05)
except KeyboardInterrupt:
    print("\n종료")
    ser.close()

import board, adafruit_dht, csv, time
from datetime import datetime

sensor = adafruit_dht.DHT22(board.D4)
FILE = "sensor_log.csv"

with open(FILE, "w", newline="") as f:
    csv.writer(f).writerow(["timestamp", "temperature", "humidity"])

try:
    while True:
        try:
            temp, hum = sensor.temperature, sensor.humidity
            if temp is None or hum is None:
                raise RuntimeError("None 반환")
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open(FILE, "a", newline="") as f:
                csv.writer(f).writerow([now, round(temp, 1), round(hum, 1)])
            print(f"{now} -> {temp:.1f}°C {hum:.1f}%")
        except RuntimeError as e:
            print(f"읽기 실패: {e}")
        time.sleep(5)
except KeyboardInterrupt:
    sensor.exit()
    print(f"저장 완료: {FILE}")

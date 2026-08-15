# 설치: pip install adafruit-circuitpython-dht
#      sudo apt install libgpiod2 -y

import board, adafruit_dht, time

sensor = adafruit_dht.DHT22(board.D4)  # GPIO4

print("DHT22 읽기 시작 (Ctrl+C로 종료)")

while True:
    try:
        temperature = sensor.temperature
        humidity = sensor.humidity
        if temperature is None or humidity is None:
            raise RuntimeError("None 반환")
        print(f"온도: {temperature:.1f}°C  습도: {humidity:.1f}%")
    except RuntimeError as e:
        print(f"읽기 실패 (재시도): {e}")
    time.sleep(2)  # 최소 샘플링 간격

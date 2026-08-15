import board, adafruit_dht, time, json, statistics
 
sensor = adafruit_dht.DHT22(board.D4)
 
def calibrate(reference_temp, n=10):
    readings = []
    for _ in range(n):
        try:
            readings.append(sensor.temperature)
        except RuntimeError:
            pass
        time.sleep(2.5)
    measured_avg = statistics.mean(readings)
    offset = reference_temp - measured_avg
    with open("dht22_calibration.json", "w") as f:
        json.dump({"temp_offset": offset}, f)
    print(f"측정 평균: {measured_avg:.2f}°C, 보정값: {offset:+.2f}°C 저장 완료")
    return offset
 
def read_calibrated():
    with open("dht22_calibration.json") as f:
        offset = json.load(f)["temp_offset"]
    return sensor.temperature + offset
 
# 1) 기준 온도계로 23.0도를 확인했다면:
# calibrate(reference_temp=23.0)
# 2) 이후 read_calibrated()로 보정된 값을 사용

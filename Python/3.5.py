import threading, time, board
import adafruit_dht, RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

shared = {
    "temp": None, "hum": None,
    "dist": None,
    "pir":  False, "last_pir": 0
}
lock = threading.Lock()

def thread_dht22():
    sensor = adafruit_dht.DHT22(board.D4)
    while True:
        try:
            t, h = sensor.temperature, sensor.humidity
            if t and h:
                with lock:
                    shared["temp"] = round(t, 1)
                    shared["hum"]  = round(h, 1)
        except RuntimeError: pass
        time.sleep(5)

def thread_ultrasonic():
    GPIO.setup(23, GPIO.OUT)
    GPIO.setup(24, GPIO.IN)
    while True:
        d = measure_stable(3)
        if d is not None:
            with lock: shared["dist"] = d
        time.sleep(0.2)

def thread_pir():
    GPIO.setup(17, GPIO.IN)
    def on_motion(ch):
        with lock:
            shared["pir"]      = True
            shared["last_pir"] = time.time()
    GPIO.add_event_detect(17, GPIO.RISING, callback=on_motion, bouncetime=3000)
    while True:
        with lock:
            if shared["pir"] and time.time() - shared["last_pir"] > 30:
                shared["pir"] = False
        time.sleep(1)

for fn in [thread_dht22, thread_ultrasonic, thread_pir]:
    threading.Thread(target=fn, daemon=True).start()

try:
    while True:
        with lock:
            t, h, d, p = shared["temp"], shared["hum"], shared["dist"], shared["pir"]
        print(f"온도:{t}°C  습도:{h}%  거리:{d}cm  PIR:{'감지!' if p else '-'}")
        time.sleep(1)
except KeyboardInterrupt:
    GPIO.cleanup()

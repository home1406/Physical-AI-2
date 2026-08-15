# Mosquitto 브로커 설치 (라즈베리파이에서)
# sudo apt install -y mosquitto mosquitto-clients
# sudo systemctl enable mosquitto
# sudo systemctl start mosquitto

# 테스트 (두 터미널)
# 터미널 1 (구독):
# mosquitto_sub -t "home/#" -v

# 터미널 2 (발행):
# mosquitto_pub -t "home/light/living" -m "ON"
import paho.mqtt.client as mqtt, json, time, RPi.GPIO as GPIO

BROKER = "localhost"

devices = {
    "light_living":  False,
    "fan_main":      False,
    "plug_tv":       False,
}

GPIO_MAP = {
    "light_living": 5,
    "fan_main":     6,
    "plug_tv":      13,
}

GPIO.setmode(GPIO.BCM)
GPIO.setup(list(GPIO_MAP.values()), GPIO.OUT)

client = mqtt.Client()

def on_message(cli, userdata, msg):
    topic   = msg.topic
    payload = msg.payload.decode()
    parts   = topic.split("/")
    if len(parts) == 3 and parts[1] == "command":
        device = parts[2]
        if device in devices:
            state = payload.upper() == "ON"
            devices[device] = state
            if device in GPIO_MAP:
                GPIO.output(GPIO_MAP[device], GPIO.HIGH if state else GPIO.LOW)
            cli.publish(f"home/status/{device}", "ON" if state else "OFF", retain=True)
            print(f"{device}: {'ON' if state else 'OFF'}")

client.on_message = on_message
client.connect(BROKER, 1883)
client.subscribe("home/command/#")
client.loop_start()

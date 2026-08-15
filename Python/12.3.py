import whisper, sounddevice as sd, numpy as np, time

COMMANDS = {
    "켜줘": "led_on",   "켜":   "led_on",
    "꺼줘": "led_off",  "꺼":   "led_off",
    "빨강": "red",      "빨간색": "red",
    "초록": "green",    "초록색": "green",
    "파랑": "blue",     "파란색": "blue",
    "전진": "forward",  "앞으로": "forward",
    "후진": "backward", "뒤로":   "backward",
    "정지": "stop",     "멈춰":   "stop",
    "빠르게": "fast",   "느리게": "slow",
}

model = whisper.load_model("base")

def record(duration=3):
    audio = sd.rec(int(duration*16000), samplerate=16000, channels=1, dtype=np.int16)
    sd.wait()
    return audio.flatten().astype(np.float32) / 32768.0

def execute(action):
    if   action == "led_on":   set_led_color(255, 255, 255)
    elif action == "led_off":  leds_off()
    elif action == "red":      set_led_color(255, 0, 0)
    elif action == "green":    set_led_color(0, 255, 0)
    elif action == "blue":     set_led_color(0, 0, 255)
    elif action == "forward":  motor_ramp("forward", 150)
    elif action == "backward": motor_ramp("backward", 150)
    elif action == "stop":     motor_stop_smooth()
    elif action == "fast":     motor_ramp("forward", 255)
    elif action == "slow":     motor_ramp("forward", 80)


leds_off(); motor_stop()
print("음성 LED·모터 제어 준비 완료. 명령을 말하세요.")

try:
    while True:
        audio  = record(3)
        result = model.transcribe(audio, language="ko", fp16=False)
        text   = result["text"].strip()
        print(f"인식: {text}")
        for kw, act in COMMANDS.items():
            if kw in text:
                print(f"실행: {act}")
                execute(act)
                break
except KeyboardInterrupt:
    leds_off(); motor_stop(); pi.stop()

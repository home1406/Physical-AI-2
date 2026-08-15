import threading, queue, time

wakeword_q = queue.Queue()
stt_q      = queue.Queue()
tts_q      = queue.Queue()

is_speaking = threading.Event()

COMMANDS = {
    "불 켜": "light_on",
    "불 꺼": "light_off",
    "온도":  "get_temp",
    "안녕":  "greet",
}

def thread_stt():
    model = whisper.load_model("base")
    while True:
        wakeword_q.get()  # 웨이크워드 대기
        audio_bytes = record_voiced_segment()
        audio_np    = np.frombuffer(audio_bytes, np.int16).astype(np.float32) / 32768.0
        result      = model.transcribe(audio_np, language="ko", fp16=False)
        text        = result["text"].strip()
        print(f"인식: {text}")
        stt_q.put(text)

def thread_command():
    while True:
        text     = stt_q.get()
        response = "명령을 이해하지 못했습니다."
        for kw, action in COMMANDS.items():
            if kw in text:
                if   action == "light_on":  response = "조명을 켰습니다."
                elif action == "light_off": response = "조명을 껐습니다."
                elif action == "get_temp":  response = "현재 온도는 25도입니다."
                elif action == "greet":     response = "안녕하세요!"
                break
        tts_q.put(response)

def thread_tts():
    while True:
        text = tts_q.get()
        is_speaking.set()
        speak(text)
        is_speaking.clear()

for fn in [thread_stt, thread_command, thread_tts]:
    threading.Thread(target=fn, daemon=True).start()

print("음성 비서 시작. 웨이크워드를 말하세요.")
# 웨이크워드 감지 후 wakeword_q.put(True) 호출하면 STT 시작

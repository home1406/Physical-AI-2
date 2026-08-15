
# pip install openai-whisper

import whisper, time

model = whisper.load_model("base")

def transcribe(audio_file, language="ko"):
    t0 = time.perf_counter()
    result = model.transcribe(
        audio_file,
        language=language,
        fp16=False,
        temperature=0,
    )
    elapsed = time.perf_counter() - t0
    text    = result["text"].strip()
    print(f"[{elapsed:.1f}초] {text}")
    return text

text = transcribe("recording.wav")
print(f"인식 결과: {text}")

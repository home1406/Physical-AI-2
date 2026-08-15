# pip install webrtcvad sounddevice

import webrtcvad, sounddevice, numpy as np, time

SAMPLE_RATE    = 16000
FRAME_DURATION = 30   # 30ms 프레임
FRAME_SIZE     = int(SAMPLE_RATE * FRAME_DURATION / 1000)

vad = webrtcvad.Vad(3)  # 민감도 0(낮음)~3(높음)

def record_voiced_segment(max_silence_sec=1.5):
    """말이 시작되면 녹음하고 침묵이 지속되면 종료한다."""
    print("말씀하세요...")
    voiced_frames  = []
    silence_frames = 0
    max_silence    = int(max_silence_sec * 1000 / FRAME_DURATION)
    recording      = False

    with sounddevice.RawInputStream(
        samplerate=SAMPLE_RATE, channels=1,
        dtype="int16", blocksize=FRAME_SIZE
    ) as stream:
        while True:
            frame, _ = stream.read(FRAME_SIZE)
            is_speech = vad.is_speech(bytes(frame), SAMPLE_RATE)

            if not recording:
                if is_speech:
                    print("음성 감지! 녹음 중...", end="", flush=True)
                    recording = True
                    voiced_frames = [bytes(frame)]
            else:
                voiced_frames.append(bytes(frame))
                if is_speech:
                    silence_frames = 0
                else:
                    silence_frames += 1
                    if silence_frames > max_silence:
                        print(" 완료")
                        break

    return b"".join(voiced_frames)


# VAD + Whisper 통합
while True:
    audio_bytes = record_voiced_segment()
    audio_np    = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
    result      = model.transcribe(audio_np, language="ko", fp16=False)
    text        = result["text"].strip()
    print(f"인식: {text}")

    if "불 켜" in text: print("→ 조명 ON")
    elif "불 꺼" in text: print("→ 조명 OFF")
    elif "종료" in text: break

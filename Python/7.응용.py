import sounddevice as sd, numpy as np, webrtcvad, collections
from faster_whisper import WhisperModel
 
vad = webrtcvad.Vad(2)  # 0(관대)~3(엄격)
model = WhisperModel("small", device="cpu", compute_type="int8")
SAMPLE_RATE = 16000
FRAME_MS = 30
FRAME_SAMPLES = SAMPLE_RATE * FRAME_MS // 1000
 
def record_utterance(max_silence_frames=15):
    """음성이 시작되면 녹음하고, 일정 시간 침묵이 지속되면 종료"""
    ring = collections.deque(maxlen=max_silence_frames)
    voiced_frames = []
    triggered = False
 
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1,
                         dtype="int16", blocksize=FRAME_SAMPLES) as stream:
        print("말씀하세요...")
        while True:
            frame, _ = stream.read(FRAME_SAMPLES)
            frame_bytes = frame.tobytes()
            is_speech = vad.is_speech(frame_bytes, SAMPLE_RATE)
 
            if not triggered:
                ring.append((frame, is_speech))
                if sum(s for _, s in ring) > 0.6 * ring.maxlen:
                    triggered = True
                    voiced_frames.extend(f for f, _ in ring)
                    ring.clear()
            else:
                voiced_frames.append(frame)
                ring.append(is_speech)
                if len(ring) == ring.maxlen and sum(ring) == 0:
                    break
    return np.concatenate(voiced_frames).flatten().astype(np.float32) / 32768.0
 
audio = record_utterance()
segments, _ = model.transcribe(audio, language="ko")
text = "".join(seg.text for seg in segments)
print("인식 결과:", text)

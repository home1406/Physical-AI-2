# 마이크 목록 확인
# arecord -l

# 테스트 녹음 (5초)
# arecord -D plughw:1,0 -f S16_LE -r 16000 -d 5 test.wav
# aplay test.wav

# Python sounddevice로 녹음
# pip install sounddevice

import sounddevice as sd, numpy as np
import scipy.io.wavfile as wavfile

SAMPLE_RATE = 16000
DURATION    = 5

print(f"{DURATION}초간 녹음...")
audio = sd.rec(int(DURATION * SAMPLE_RATE),
               samplerate=SAMPLE_RATE, channels=1, dtype=np.int16)
sd.wait()

wavfile.write("recording.wav", SAMPLE_RATE, audio)
print("recording.wav 저장 완료")

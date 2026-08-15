# pip install TTS

from TTS.api import TTS
import sounddevice as sd
from scipy.io import wavfile

tts = TTS(model_name="tts_models/ko/css10/vits")

def speak(text):
    print(f"TTS: {text}")
    tts.tts_to_file(text=text, file_path="/tmp/tts.wav")
    sr, audio = wavfile.read("/tmp/tts.wav")
    sd.play(audio, sr)
    sd.wait()

speak("안녕하세요. 저는 라즈베리파이 음성 비서입니다.")
speak("현재 온도는 25.3도입니다.")

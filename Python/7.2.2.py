# pip install faster-whisper

from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe_fast(audio_path, language="ko"):
    segments, info = model.transcribe(
        audio_path,
        language=language,
        beam_size=1,
        vad_filter=True
    )
    return " ".join([seg.text for seg in segments]).strip()

import numpy as np
 
def normalize_audio(audio: np.ndarray, target_dbfs=-20.0) -> np.ndarray:
    """오디오 배열(float32, -1~1)을 목표 dBFS 레벨로 정규화"""
    rms = np.sqrt(np.mean(audio ** 2))
    if rms < 1e-6:
        return audio  # 완전한 무음은 그대로 반환
    current_dbfs = 20 * np.log10(rms)
    gain_db = target_dbfs - current_dbfs
    gain = 10 ** (gain_db / 20)
    normalized = audio * gain
    return np.clip(normalized, -1.0, 1.0)
 
# 사용 예 (7.1절에서 녹음한 audio 배열 재사용)
# raw_audio = record_utterance()
# before_peak = np.max(np.abs(raw_audio))
# audio = normalize_audio(raw_audio, target_dbfs=-20.0)
# after_peak = np.max(np.abs(audio))
# print(f"정규화 전 최대진폭 {before_peak:.3f} -> 후 {after_peak:.3f}")

from collections import deque
import numpy as np


class MovingAverage:
    """이동 평균 필터 -- 최근 N개 값의 평균"""

    def __init__(self, window_size=5):
        self.window = deque(maxlen=window_size)

    def update(self, value):
        self.window.append(value)
        return sum(self.window) / len(self.window)


class MedianFilter:
    """중앙값 필터 -- 이상값 제거"""

    def __init__(self, window_size=5):
        self.window = deque(maxlen=window_size)

    def update(self, value):
        self.window.append(value)
        return float(np.median(self.window))


class EMA:
    """지수 이동 평균 -- 최근 값에 더 높은 가중치"""

    def __init__(self, alpha=0.2):
        self.alpha = alpha
        self._value = None

    def update(self, value):
        if self._value is None:
            self._value = value
        else:
            self._value = self.alpha * value + (1 - self.alpha) * self._value
        return self._value


if __name__ == "__main__":
    ma = MovingAverage(5)
    med = MedianFilter(5)
    ema = EMA(alpha=0.2)

    for raw in [100.0, 99.8, 97.3, 100.5, 99.9, 130.0, 100.1]:
        print(f"원본 {raw:6.1f}  MA {ma.update(raw):6.1f}  "
              f"중앙값 {med.update(raw):6.1f}  EMA {ema.update(raw):6.1f}")

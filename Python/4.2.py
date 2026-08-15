import cv2, time

img  = cv2.imread("test.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 각 필터 적용
gauss     = cv2.GaussianBlur(gray, (7,7), 0)
median_f  = cv2.medianBlur(gray, 7)
bilateral = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

# 처리 시간 비교
for name, fn in [
    ("GaussianBlur(7,7)", lambda: cv2.GaussianBlur(gray, (7,7), 0)),
    ("medianBlur(7)",     lambda: cv2.medianBlur(gray, 7)),
    ("bilateralFilter",  lambda: cv2.bilateralFilter(img, 9, 75, 75)),
]:
    t = time.perf_counter()
    for _ in range(100): fn()
    ms = (time.perf_counter() - t) * 10
    print(f"{name:22s}: {ms:.2f}ms")

# 솔트-페퍼 노이즈 추가 후 PSNR 비교
import numpy as np
noisy = gray.copy()
n = int(noisy.size * 0.02)
noisy.flat[np.random.randint(0, noisy.size, n)] = 255
noisy.flat[np.random.randint(0, noisy.size, n)] = 0

g_dn = cv2.GaussianBlur(noisy, (7,7), 0)
m_dn = cv2.medianBlur(noisy, 7)
print(f"가우시안 PSNR: {cv2.PSNR(gray, g_dn):.1f}dB")
print(f"미디안  PSNR: {cv2.PSNR(gray, m_dn):.1f}dB")  # 미디안이 더 높음
필터 선택 가이드
─────────────────────────────────────────────────────────────────────
필터              속도      노이즈 종류      엣지 보존   사용 상황
─────────────────────────────────────────────────────────────────────
GaussianBlur      빠름      가우시안 노이즈  약함        Canny 전처리
medianBlur        중간      솔트-페퍼        강함        카메라 결함점
bilateralFilter   느림      가우시안 노이즈  매우 강함   얼굴인식 전처리
─────────────────────────────────────────────────────────────────────

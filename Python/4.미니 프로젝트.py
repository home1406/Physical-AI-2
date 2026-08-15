import cv2, cv2.aruco as aruco, numpy as np
 
MARKER_SIZE_CM = 5.0  # 실제 인쇄한 마커의 한 변 길이
FOCAL_LENGTH_PX = 600  # 카메라 캘리브레이션으로 얻은 초점거리(근사값)
 
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
detector = aruco.ArucoDetector(aruco_dict, aruco.DetectorParameters())
 
def estimate_distance(corner):
    """마커의 픽셀 폭으로부터 카메라까지의 거리를 근사 계산"""
    pts = corner[0]
    side_px = np.mean([
        np.linalg.norm(pts[0] - pts[1]),
        np.linalg.norm(pts[1] - pts[2]),
    ])
    if side_px < 1:
        return None
    return (MARKER_SIZE_CM * FOCAL_LENGTH_PX) / side_px
 
cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
    if ids is not None:
        for corner, mid in zip(corners, ids.flatten()):
            dist_cm = estimate_distance(corner)
            aruco.drawDetectedMarkers(frame, [corner])
            if dist_cm:
                cx, cy = corner[0].mean(axis=0).astype(int)
                cv2.putText(frame, f"{dist_cm:.1f}cm", (cx, cy),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Distance Estimator", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
cap.release()
cv2.destroyAllWindows()

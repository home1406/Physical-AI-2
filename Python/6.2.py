import mediapipe as mp, cv2, numpy as np, time
from picamera2 import Picamera2

mp_pose    = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

def angle(a, b, c):
    """세 점으로 이뤄진 각도 계산 (b가 꼭짓점)"""
    a, b, c = np.array(a), np.array(b), np.array(c)
    ba, bc  = a - b, c - b
    cos_a   = np.dot(ba, bc) / (np.linalg.norm(ba)*np.linalg.norm(bc) + 1e-8)
    return np.degrees(np.arccos(np.clip(cos_a, -1.0, 1.0)))


cam = Picamera2()
cam.configure(cam.create_video_configuration(main={"size":(640,480),"format":"RGB888"}))
cam.start()

# 팔굽혀펴기 카운터
counter = 0
stage   = "up"  # up / down

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while True:
        frame   = cam.capture_array()
        results = pose.process(frame)
        bgr     = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if results.pose_landmarks:
            lm = results.pose_landmarks.landmark
            h, w = bgr.shape[:2]
            get  = lambda i: [lm[i].x*w, lm[i].y*h]

            r_ang = angle(
                get(mp_pose.PoseLandmark.RIGHT_SHOULDER),
                get(mp_pose.PoseLandmark.RIGHT_ELBOW),
                get(mp_pose.PoseLandmark.RIGHT_WRIST)
            )

            # 팔굽혀펴기 카운터 로직
            if r_ang < 50 and stage == "up":
                stage = "down"
            if r_ang > 160 and stage == "down":
                stage = "up"
                counter += 1
                print(f"팔굽혀펴기 {counter}회!")

            cv2.putText(bgr, f"각도: {r_ang:.0f}°",
                        tuple(map(int, get(mp_pose.PoseLandmark.RIGHT_ELBOW))),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,255,0), 2)

            mp_drawing.draw_landmarks(
                bgr, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        cv2.putText(bgr, f"팔굽혀펴기: {counter}회  {stage}",
                    (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0,0,255), 2)
        cv2.imshow("MediaPipe Pose", bgr)
        if cv2.waitKey(1) & 0xFF == ord("q"): break

cam.stop()
cv2.destroyAllWindows()

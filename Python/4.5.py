import cv2, time
from picamera2 import Picamera2

HAARCASCADES  = cv2.data.haarcascades
face_cascade  = cv2.CascadeClassifier(HAARCASCADES + "haarcascade_frontalface_default.xml")
eye_cascade   = cv2.CascadeClassifier(HAARCASCADES + "haarcascade_eye.xml")

cam = Picamera2()
cam.configure(cam.create_video_configuration(main={"size":(640,480),"format":"RGB888"}))
cam.start()

fps = 0; fps_cnt = 0; fps_t = time.perf_counter()

while True:
    frame = cam.capture_array()
    gray  = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    gray  = cv2.equalizeHist(gray)  # 조명 불균일 보정

    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=4, minSize=(50,50))

    result = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    for (fx, fy, fw, fh) in faces:
        cv2.rectangle(result, (fx,fy), (fx+fw,fy+fh), (255,0,0), 2)
        cv2.putText(result, "Face", (fx, fy-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,0,0), 2)

        # ROI 안에서 눈 찾기
        roi_gray  = gray[fy:fy+fh, fx:fx+fw]
        roi_color = result[fy:fy+fh, fx:fx+fw]
        eyes = eye_cascade.detectMultiScale(
            roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(20,20))
        for (ex, ey, ew, eh) in eyes[:2]:
            cv2.rectangle(roi_color, (ex,ey), (ex+ew,ey+eh), (0,255,0), 2)

    fps_cnt += 1
    if time.perf_counter() - fps_t >= 1:
        fps = fps_cnt; fps_cnt = 0; fps_t = time.perf_counter()

    cv2.putText(result, f"얼굴:{len(faces)}명  FPS:{fps}",
                (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
    cv2.imshow("Face Detection", result)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cam.stop()
cv2.destroyAllWindows()

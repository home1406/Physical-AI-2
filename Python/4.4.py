import cv2, numpy as np, time
from picamera2 import Picamera2

cam = Picamera2()
cam.configure(cam.create_video_configuration(
    main={"size": (640,480), "format": "RGB888"}))
cam.start()

COLOR_RANGES = {
    "red":    [(  0,100,100), ( 10,255,255)],
    "red2":   [(160,100,100), (180,255,255)],
    "green":  [( 40, 80, 80), ( 90,255,255)],
    "blue":   [(100,100, 80), (130,255,255)],
    "yellow": [( 20,100,100), ( 40,255,255)],
}

def track_color(frame_rgb, color):
    hsv  = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
    l, u = COLOR_RANGES[color]
    mask = cv2.inRange(hsv, np.array(l), np.array(u))
    if color == "red":
        l2, u2 = COLOR_RANGES["red2"]
        mask  |= cv2.inRange(hsv, np.array(l2), np.array(u2))
    kernel = np.ones((5,5), np.uint8)
    mask   = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
    mask   = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours: return None
    c = max(contours, key=cv2.contourArea)
    if cv2.contourArea(c) < 1000: return None
    return cv2.boundingRect(c)

while True:
    frame = cam.capture_array()
    bgr   = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    bbox = track_color(frame, "green")
    if bbox:
        x, y, w, h = bbox
        cx, cy = x+w//2, y+h//2
        cv2.rectangle(bgr, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.circle(bgr, (cx,cy), 5, (0,0,255), -1)
        cv2.putText(bgr, f"({cx},{cy})", (x,y-10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

    cv2.imshow("Color Tracking", bgr)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cam.stop()
cv2.destroyAllWindows()

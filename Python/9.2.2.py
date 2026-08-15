import pigpio, cv2, time
from picamera2 import Picamera2

pi   = pigpio.pi()
pan  = Servo(gpio_pin=18, pi=pi)
tilt = Servo(gpio_pin=13, pi=pi)

pid_pan  = PID(Kp=0.08, Ki=0.001, Kd=0.02, setpoint=0, output_min=-30, output_max=30)
pid_tilt = PID(Kp=0.08, Ki=0.001, Kd=0.02, setpoint=0, output_min=-30, output_max=30)

pan.angle = tilt.angle = 90

cam = Picamera2()
cam.configure(cam.create_video_configuration(main={"size":(640,480),"format":"RGB888"}))
cam.start()

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

while True:
    frame = cam.capture_array()
    gray  = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(
        gray, scaleFactor=1.1, minNeighbors=4, minSize=(60,60))

    bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

    if len(faces) > 0:
        x, y, w, h = max(faces, key=lambda b: b[2]*b[3])
        cx = x + w//2
        cy = y + h//2

        pan.angle  += pid_pan.compute(-(cx - 320))
        tilt.angle += pid_tilt.compute(-(cy - 240))

        cv2.rectangle(bgr, (x,y), (x+w,y+h), (0,255,0), 2)
        cv2.circle(bgr, (cx,cy), 5, (0,0,255), -1)

    cv2.imshow("Face Tracking", bgr)
    if cv2.waitKey(1) & 0xFF == ord("q"): break

cam.stop()
pi.stop()

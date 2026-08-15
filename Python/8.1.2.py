pi    = pigpio.pi()
pan   = Servo(gpio_pin=18, pi=pi)  # 좌우
tilt  = Servo(gpio_pin=13, pi=pi)  # 상하

pan.angle  = 90
tilt.angle = 90
time.sleep(0.5)

def track_face(cx, cy, frame_w=640, frame_h=480):
    err_x = cx - frame_w // 2
    err_y = cy - frame_h // 2
    pan.angle  = max(0, min(180, pan.angle  - err_x * 0.05))
    tilt.angle = max(0, min(180, tilt.angle + err_y * 0.05))

import face_recognition, cv2, pickle, os, time
import RPi.GPIO as GPIO
from picamera2 import Picamera2

DOOR_PIN    = 24
UNLOCK_TIME = 5

GPIO.setup(DOOR_PIN, GPIO.OUT)
GPIO.output(DOOR_PIN, GPIO.LOW)

def load_faces():
    known = {}
    for fn in os.listdir("faces"):
        if fn.endswith(".pkl"):
            with open(f"faces/{fn}", "rb") as f:
                known[fn[:-4]] = pickle.load(f)
    print(f"얼굴 데이터: {list(known.keys())}")
    return known

def recognize(cam, known, last_unlock):
    frame = cam.capture_array()
    locs  = face_recognition.face_locations(frame, model="hog")
    encs  = face_recognition.face_encodings(frame, locs)

    for enc in encs:
        best = None; best_d = 0.6
        for name, known_encs in known.items():
            dists = face_recognition.face_distance(known_encs, enc)
            if min(dists) < best_d:
                best_d = min(dists); best = name
        now = time.time()
        if best and now - last_unlock > UNLOCK_TIME + 5:
            print(f"인식: {best} — 잠금 해제")
            GPIO.output(DOOR_PIN, GPIO.HIGH)
            time.sleep(UNLOCK_TIME)
            GPIO.output(DOOR_PIN, GPIO.LOW)
            return now
        elif not best:
            print("미등록 방문자 — 알림 전송")
    return last_unlock

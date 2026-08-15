class LaneFollower:
    def __init__(self):
        self.lane = LaneDetector()
        self.car  = MiniCar()
        self.cam  = self._init_camera()
        self.log  = []
        self.Kp   = 0.15
        self.Kd   = 0.08
        self._prev_error = 0
        self._prev_time  = time.perf_counter()

    def _init_camera(self):
        from picamera2 import Picamera2
        cam = Picamera2()
        cam.configure(cam.create_video_configuration(
            main={"size":(320,240), "format":"RGB888"}))
        cam.start(); time.sleep(0.3)
        return cam

    def _compute(self, error):
        now = time.perf_counter()
        dt  = max(now - self._prev_time, 1e-6)
        p   = self.Kp * error
        d   = self.Kd * (error - self._prev_error) / dt
        self._prev_error = error
        self._prev_time  = now
        steer = -(p + d)
        return max(-1.0, min(1.0, steer / 160))

    def _apply(self, steer, base=60):
        l = int(base * (1 + steer))
        r = int(base * (1 - steer))
        self.car.left.forward(max(0, min(100, l)))
        self.car.right.forward(max(0, min(100, r)))
        return l, r

    def drive(self, duration=60):
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < duration:
            frame = self.cam.capture_array()
            cx, error = self.lane.detect(frame)
            if cx is None:
                self.car.forward(30)
            else:
                steer = self._compute(error)
                l, r  = self._apply(steer)
                self.log.append({
                    "t": time.perf_counter()-t0,
                    "error": error,
                    "steer": steer,
                    "left": l, "right": r
                })
        self.car.stop()
        self._save_log()

    def _save_log(self):
        import csv
        with open("drive_log.csv", "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=["t","error","steer","left","right"])
            w.writeheader(); w.writerows(self.log)
        print(f"주행 로그 저장: drive_log.csv ({len(self.log)}행)")

import time
 
class PID:
    def __init__(self, Kp, Ki, Kd, setpoint=0):
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.setpoint = setpoint
        self.integral = 0.0
        self.prev_error = 0.0
        self.prev_time = time.perf_counter()
 
    def compute(self, measurement):
        now = time.perf_counter()
        dt = max(now - self.prev_time, 1e-3)
        error = self.setpoint - measurement
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt
        output = self.Kp*error + self.Ki*self.integral + self.Kd*derivative
        self.prev_error, self.prev_time = error, now
        return output
 
def simulate(Kp, Ki, Kd, steps=200):
    """단순 1차 시스템으로 게인 조합을 시뮬레이션 평가"""
    pid = PID(Kp, Ki, Kd, setpoint=100)
    value = 0.0
    overshoot = 0.0
    for _ in range(steps):
        output = pid.compute(value)
        value += output * 0.05  # 단순화된 플랜트 응답
        overshoot = max(overshoot, value - 100)
        time.sleep(0.001)
    final_error = abs(100 - value)
    return final_error, overshoot
 
candidates = [(0.5,0.0,0.0),(0.8,0.1,0.05),(1.2,0.2,0.1),(0.6,0.05,0.2)]
print(f"{'Kp':>5}{'Ki':>6}{'Kd':>6}{'최종오차':>10}{'오버슈트':>10}")
for Kp, Ki, Kd in candidates:
    err, over = simulate(Kp, Ki, Kd)
    print(f"{Kp:5.2f}{Ki:6.2f}{Kd:6.2f}{err:10.2f}{over:10.2f}")

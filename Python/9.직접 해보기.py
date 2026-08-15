import matplotlib.pyplot as plt
 
class PID:
    def __init__(self, Kp, Ki, Kd, setpoint, integral_limit=None):
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self.setpoint = setpoint
        self.integral = 0.0
        self.prev_error = 0.0
        self.integral_limit = integral_limit  # None이면 windup 방지 없음
 
    def compute(self, measurement, dt=0.05):
        error = self.setpoint - measurement
        self.integral += error * dt
        if self.integral_limit is not None:
            self.integral = max(-self.integral_limit,
                                 min(self.integral_limit, self.integral))
        derivative = (error - self.prev_error) / dt
        self.prev_error = error
        return self.Kp*error + self.Ki*self.integral + self.Kd*derivative
 
def simulate(pid, steps=150):
    value = 0.0
    history = []
    for _ in range(steps):
        output = pid.compute(value)
        value += output * 0.02
        history.append(value)
    return history
 
without_clamp = simulate(PID(1.5, 0.8, 0.1, setpoint=100, integral_limit=None))
with_clamp = simulate(PID(1.5, 0.8, 0.1, setpoint=100, integral_limit=30))
 
plt.plot(without_clamp, label="클램핑 없음 (오버슈트 큼)")
plt.plot(with_clamp, label="클램핑 적용 (안정적)")
plt.axhline(100, color="gray", linestyle="--", label="목표값")
plt.legend(); plt.xlabel("스텝"); plt.ylabel("값")
plt.title("적분 클램핑(anti-windup) 유무 비교")
plt.savefig("antiwindup_compare.png", dpi=150)
print("그래프 저장: antiwindup_compare.png")

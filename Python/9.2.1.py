import time

class PID:
    """이산 시간 PID 제어기 (Anti-windup 적용)"""

    def __init__(self, Kp, Ki, Kd, setpoint=0,
                 output_min=-100, output_max=100,
                 integral_limit=50):
        self.Kp = Kp; self.Ki = Ki; self.Kd = Kd
        self.setpoint       = setpoint
        self.output_min     = output_min
        self.output_max     = output_max
        self.integral_limit = integral_limit
        self._integral   = 0.0
        self._prev_error = 0.0
        self._prev_time  = time.perf_counter()

    def compute(self, measurement):
        now = time.perf_counter()
        dt  = max(now - self._prev_time, 1e-6)

        error = self.setpoint - measurement

        p_term = self.Kp * error

        # I항 (Anti-windup: 출력 포화 시 적분 멈춤)
        self._integral += error * dt
        self._integral  = max(-self.integral_limit,
                          min( self.integral_limit, self._integral))
        i_term = self.Ki * self._integral

        # D항 (측정값 미분)
        d_term = self.Kd * (error - self._prev_error) / dt

        output = p_term + i_term + d_term
        output = max(self.output_min, min(self.output_max, output))

        self._prev_error = error
        self._prev_time  = now

        return output

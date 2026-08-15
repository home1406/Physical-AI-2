import csv, time
 
class PIDLogger:
    def __init__(self, pid, filepath="pid_log.csv"):
        self.pid = pid
        self.filepath = filepath
        self.rows = []
 
    def step(self, measurement):
        output = self.pid.compute(measurement)
        self.rows.append({
            "time": time.perf_counter(),
            "setpoint": self.pid.setpoint,
            "measurement": measurement,
            "error": self.pid.setpoint - measurement,
            "output": output,
        })
        return output
 
    def save(self):
        if not self.rows:
            return
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
            writer.writeheader()
            writer.writerows(self.rows)
        print(f"{len(self.rows)}개 샘플을 {self.filepath}에 저장했습니다")
 
    def settling_time(self, tolerance=2.0):
        """오차가 tolerance 이내로 안정된 첫 시각을 반환"""
        start = self.rows[0]["time"]
        for row in self.rows:
            if abs(row["error"]) <= tolerance:
                return row["time"] - start
        return None

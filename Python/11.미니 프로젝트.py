import csv, time
 
class DriveLogger:
    def __init__(self, filepath="drive_log.csv"):
        self.filepath = filepath
        self.rows = []
        self.start_time = time.perf_counter()
 
    def log(self, steer_error, left_speed, right_speed, obstacle_dist):
        self.rows.append({
            "t": round(time.perf_counter() - self.start_time, 2),
            "error": steer_error,
            "left": left_speed,
            "right": right_speed,
            "obstacle_cm": obstacle_dist,
        })
 
    def save(self):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.rows[0].keys())
            writer.writeheader()
            writer.writerows(self.rows)
 
    def summary(self):
        errors = [abs(r["error"]) for r in self.rows]
        stops = sum(1 for r in self.rows if r["obstacle_cm"] and r["obstacle_cm"] < 20)
        return {
            "평균 조향오차": sum(errors) / len(errors) if errors else 0,
            "최대 조향오차": max(errors) if errors else 0,
            "급정지 횟수": stops,
            "총 주행시간(초)": self.rows[-1]["t"] if self.rows else 0,
        }
 
logger = DriveLogger()
# 주행 루프 안에서: logger.log(error, left_speed, right_speed, dist)
# 종료 후:
# logger.save()
# print(logger.summary())

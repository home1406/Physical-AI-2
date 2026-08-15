class Rule:
    def __init__(self, name, condition_fn, action_fn, cooldown=60):
        self.name = name
        self.condition_fn = condition_fn
        self.action_fn = action_fn
        self.cooldown = cooldown
        self.last_fired = 0
 
    def evaluate(self, state, now):
        if now - self.last_fired < self.cooldown:
            return False
        if self.condition_fn(state):
            self.action_fn(state)
            self.last_fired = now
            return True
        return False
 
def AND(*conditions):
    return lambda state: all(c(state) for c in conditions)
 
def OR(*conditions):
    return lambda state: any(c(state) for c in conditions)
 
# 조건 정의
is_hot = lambda s: s.get("temp", 0) >= 30
is_occupied = lambda s: s.get("pir", False)
is_night_time = lambda s: s.get("hour", 12) >= 22 or s.get("hour", 12) < 6
 
# 규칙: 덥고 사람이 있을 때만 에어컨 켜기
rules = [
    Rule("에어컨 자동", AND(is_hot, is_occupied),
         lambda s: print("에어컨 ON"), cooldown=300),
    Rule("야간 조명", AND(is_occupied, is_night_time),
         lambda s: print("조명 ON (야간)"), cooldown=60),
]
 
import time
state = {"temp": 31, "pir": True, "hour": 23}
now = time.time()
for rule in rules:
    fired = rule.evaluate(state, now)
    print(f"{rule.name}: {'발동' if fired else '조건 미충족 또는 쿨다운'}")

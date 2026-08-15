import time, collections
 
class RuleStats:
    def __init__(self):
        self.fire_count = collections.Counter()
        self.last_fired = {}
 
    def record(self, rule_name):
        self.fire_count[rule_name] += 1
        self.last_fired[rule_name] = time.strftime("%H:%M:%S")
 
    def report(self):
        print("규칙 발동 통계")
        print("-" * 40)
        for name, count in self.fire_count.most_common():
            print(f"{name:20s} {count:4d}회  마지막: {self.last_fired[name]}")
 
stats = RuleStats()
# 규칙 엔진의 Rule.evaluate()가 True를 반환할 때마다:
# stats.record(rule.name)
stats.record("에어컨 자동")
stats.record("에어컨 자동")
stats.record("야간 조명")
stats.report()

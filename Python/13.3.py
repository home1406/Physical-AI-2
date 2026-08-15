import time
from datetime import datetime

class AutomationRule:
    def __init__(self, name, condition_fn, action_fn, cooldown=60):
        self.name      = name
        self.condition = condition_fn
        self.action    = action_fn
        self.cooldown  = cooldown
        self._last     = 0

    def evaluate(self, state):
        if time.time() - self._last < self.cooldown: return
        if self.condition(state):
            self.action(state)
            self._last = time.time()
            print(f"[자동화] {self.name} 실행")


def get_rules(cli):
    return [
        AutomationRule(
            "고온 팬 자동 ON",
            lambda s: s.get("temp",0) > 28,
            lambda s: cli.publish("home/command/fan_main", "ON"),
            cooldown=120
        ),
        AutomationRule(
            "심야 조명 소등",
            lambda s: datetime.now().hour >= 23,
            lambda s: cli.publish("home/command/light_living", "OFF"),
            cooldown=3600
        ),
    ]


rules = get_rules(client)

while True:
    state = {"temp": read_temp(), "hum": read_hum()}
    for rule in rules:
        rule.evaluate(state)
    time.sleep(10)

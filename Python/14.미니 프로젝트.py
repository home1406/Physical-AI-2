import collections
 
class ContextualAgent:
    """최근 N턴의 대화를 기억해 '그거', '아까 그것'같은 대명사 참조를 해석"""
    def __init__(self, max_turns=5):
        self.history = collections.deque(maxlen=max_turns)
        self.last_target = None
 
    def resolve(self, user_text):
        if any(word in user_text for word in ["그거", "그것", "아까"]):
            if self.last_target:
                resolved = user_text + f" (참조 대상: {self.last_target})"
                return resolved
        return user_text
 
    def update_target(self, target_name):
        self.last_target = target_name
 
    def turn(self, user_text, target_name=None):
        resolved = self.resolve(user_text)
        self.history.append((user_text, resolved))
        if target_name:
            self.update_target(target_name)
        return resolved
 
agent = ContextualAgent()
print(agent.turn("거실 조명 켜줘", target_name="거실 조명"))
print(agent.turn("그거 다시 꺼줘"))  # '거실 조명'을 참조하는 것으로 해석

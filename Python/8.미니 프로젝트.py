import time
from enum import Enum, auto
 
class State(Enum):
    IDLE = auto()
    MOVING = auto()
    STOPPED_SAFE = auto()
    ERROR = auto()
 
class MotorStateMachine:
    def __init__(self):
        self.state = State.IDLE
        self.last_command_time = 0
 
    def command(self, action, obstacle_detected=False):
        if obstacle_detected:
            self.state = State.STOPPED_SAFE
            print("장애물 감지 -> 안전 정지")
            return
 
        if self.state == State.ERROR:
            print("오류 상태입니다. reset()을 먼저 호출하세요")
            return
 
        if action == "move" and self.state in (State.IDLE, State.STOPPED_SAFE):
            self.state = State.MOVING
            self.last_command_time = time.time()
            print("이동 시작")
        elif action == "stop":
            self.state = State.IDLE
            print("정지")
        else:
            print(f"'{action}'은 현재 상태({self.state.name})에서 허용되지 않음")
 
    def reset(self):
        self.state = State.IDLE
        print("상태 초기화 완료")
 
fsm = MotorStateMachine()
fsm.command("move")
fsm.command("move", obstacle_detected=True)  # 이동 중 장애물 감지
fsm.command("move")  # STOPPED_SAFE에서 재시작 가능
fsm.command("stop")

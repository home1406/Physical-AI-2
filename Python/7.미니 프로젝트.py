import difflib
 
COMMAND_MAP = {
    "불 켜줘": ("light", "on"),
    "불 꺼줘": ("light", "off"),
    "온도 알려줘": ("query", "temp"),
    "정지": ("emergency", "stop"),
}
 
def match_command(text, cutoff=0.6):
    """STT 결과가 정확히 일치하지 않아도 가장 비슷한 명령을 찾는다"""
    candidates = list(COMMAND_MAP.keys())
    best = difflib.get_close_matches(text, candidates, n=1, cutoff=cutoff)
    if best:
        return COMMAND_MAP[best[0]], best[0]
    return None, None
 
def handle(action, target):
    if action == "emergency":
        print("!! 비상 정지 !!")
    elif action == "light":
        print(f"조명 {target}")
    elif action == "query":
        print("현재 온도: 24.5도")
 
# STT가 '정지' 대신 '정지해'처럼 인식해도 매칭되도록 실험
for heard in ["불 좀 켜줘", "정지해", "온도가 어떻게 되나요"]:
    cmd, matched = match_command(heard)
    if cmd:
        print(f"인식: '{heard}' -> 매칭: '{matched}'")
        handle(*cmd)
    else:
        print(f"인식: '{heard}' -> 매칭 실패")

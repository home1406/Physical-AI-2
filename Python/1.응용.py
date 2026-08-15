import serial, json, time
 
class CommandLink:
    """id 기반 명령-응답 매칭 + 자동 재시도 Serial 링크"""
    def __init__(self, port="/dev/ttyUSB0", baud=115200, timeout=1.0):
        self.ser = serial.Serial(port, baud, timeout=timeout)
        time.sleep(2)  # 아두이노 리셋 대기
        self._next_id = 1
 
    def send(self, cmd: dict, retries=3):
        """명령을 보내고 같은 id의 응답을 받을 때까지 재시도"""
        cmd["id"] = self._next_id
        self._next_id += 1
        payload = (json.dumps(cmd) + "\n").encode("utf-8")
        for attempt in range(1, retries + 1):
            self.ser.write(payload)
            line = self.ser.readline().decode("utf-8", errors="ignore").strip()
            if not line:
                print(f"[재시도 {attempt}/{retries}] 응답 없음")
                continue
            try:
                resp = json.loads(line)
            except json.JSONDecodeError:
                continue
            if resp.get("id") == cmd["id"]:
                return resp
        raise TimeoutError(f"명령 {cmd}에 대한 응답을 받지 못했습니다")
 
    def close(self):
        self.ser.close()
 
# 사용 예
link = CommandLink()
result = link.send({"cmd": "servo", "pin": 9, "angle": 90})
print("응답:", result)
link.close()

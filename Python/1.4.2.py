# ── 라즈베리파이: 명령 전송 + 응답 수신 ─────────────────
import serial, json, time

def send_command(ser, cmd_dict, timeout=1.0, retries=3):
    """
    아두이노에 JSON 명령을 보내고 응답 딕셔너리를 반환한다.
    timeout: 응답 대기 최대 시간(초)
    retries: 타임아웃 시 재시도 횟수
    """
    for attempt in range(retries):
        ser.reset_input_buffer()  # 수신 버퍼 초기화

        # 명령 전송 (JSON + 줄바꿈)
        payload = (json.dumps(cmd_dict) + "\n").encode("utf-8")
        ser.write(payload)
        ser.flush()

        # 응답 대기
        t0 = time.perf_counter()
        while time.perf_counter() - t0 < timeout:
            if ser.in_waiting:
                resp = ser.readline().decode("utf-8", errors="ignore").strip()
                if resp:
                    try:
                        return json.loads(resp)
                    except json.JSONDecodeError:
                        pass  # 유효하지 않은 응답 무시
            time.sleep(0.005)

        print(f"[경고] 응답 없음 ({attempt+1}/{retries}회)")
        time.sleep(0.1)

    return {"error": "timeout", "attempts": retries}


# 사용 예시
ser = serial.Serial("/dev/ttyUSB0", 115200, timeout=1)
time.sleep(2)

r = send_command(ser, {"cmd": "led", "pin": 13, "state": 1})
print(r)  # → {"status":"ok","cmd":"led"}

r = send_command(ser, {"cmd": "servo", "pin": 9, "angle": 90})
print(r)  # → {"status":"ok","angle":90}

r = send_command(ser, {"cmd": "get_temp"})
print(r)  # → {"status":"ok","temp":25.3,"hum":61.2}

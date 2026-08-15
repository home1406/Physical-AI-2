from openai import OpenAI
import RPi.GPIO as GPIO, json, time

client = OpenAI(api_key="sk-...")  # API 키

GPIO.setmode(GPIO.BCM)

def read_temperature():
    return {"temperature": 27.3, "humidity": 62.1}

def control_device(device, state):
    GPIO_MAP = {"fan": 24, "light": 23}
    if device not in GPIO_MAP:
        return {"success": False, "error": f"알 수 없는 기기: {device}"}
    GPIO.setup(GPIO_MAP[device], GPIO.OUT)
    GPIO.output(GPIO_MAP[device], GPIO.HIGH if state else GPIO.LOW)
    return {"success": True, "device": device, "state": "ON" if state else "OFF"}


TOOLS = [
    {"type": "function", "function": {
        "name": "read_temperature",
        "description": "현재 실내 온도와 습도를 읽는다",
        "parameters": {"type": "object", "properties": {}}
    }},
    {"type": "function", "function": {
        "name": "control_device",
        "description": "스마트홈 기기를 켜거나 끈다",
        "parameters": {
            "type": "object",
            "properties": {
                "device": {"type": "string", "enum": ["fan","light"]},
                "state":  {"type": "boolean"}
            },
            "required": ["device", "state"]
        }
    }}
]

FUNS = {"read_temperature": read_temperature,
        "control_device":   control_device}


def run_agent(user_input):
    messages = [
        {"role": "system",  "content": "당신은 스마트홈 AI 어시스턴트다."},
        {"role": "user",    "content": user_input}
    ]
    for _ in range(5):
        resp = client.chat.completions.create(
            model="gpt-4o-mini", messages=messages,
            tools=TOOLS, tool_choice="auto")
        msg = resp.choices[0].message
        if msg.tool_calls:
            messages.append(msg)
            for tc in msg.tool_calls:
                fn   = tc.function.name
                args = json.loads(tc.function.arguments)
                res  = FUNS[fn](**args)
                messages.append({
                    "role": "tool", "tool_call_id": tc.id,
                    "content": json.dumps(res, ensure_ascii=False)})
        else:
            return msg.content
    return "최대 반복 횟수 초과"


for q in ["지금 온도가 몇 도야?",
          "온도 확인하고 28도 넘으면 팬 켜줘",
          "불 꺼줘"]:
    print(f"\n사용자: {q}")
    print(f"AI: {run_agent(q)}")

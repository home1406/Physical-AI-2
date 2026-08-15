import json, time
 
LOG_FILE = "agent_calls.jsonl"
 
def log_call(func_name, args, result=None, error=None):
    entry = {
        "time": time.time(),
        "function": func_name,
        "args": args,
        "result": str(result) if result is not None else None,
        "error": str(error) if error else None,
    }
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
 
def replay_log(dry_run_fn):
    """기록된 호출을 순서대로 재생 (dry_run_fn으로 시뮬레이션 실행)"""
    with open(LOG_FILE, encoding="utf-8") as f:
        for line in f:
            entry = json.loads(line)
            print(f"[리플레이] {entry['function']}({entry['args']})"
                  f" -> 원래 결과: {entry['result']}")
            dry_run_fn(entry["function"], entry["args"])
 
def dry_run(func_name, args):
    print("  (시뮬레이션 실행만 함, 실제 하드웨어 제어 없음)")
 
# 사용 예
# log_call("set_led", {"pin": 17, "state": 1}, result="ok")
# replay_log(dry_run)

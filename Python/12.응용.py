import json, os, time
 
PRESET_FILE = "presets.json"
 
def load_presets():
    if os.path.exists(PRESET_FILE):
        with open(PRESET_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}
 
def save_preset(name, led_rgb, motor_direction, motor_speed):
    presets = load_presets()
    presets[name] = {"led": led_rgb, "direction": motor_direction, "speed": motor_speed}
    with open(PRESET_FILE, "w", encoding="utf-8") as f:
        json.dump(presets, f, ensure_ascii=False, indent=2)
    print(f"프리셋 '{name}' 저장 완료: {presets[name]}")
 
def play_sequence(names, pause=0.5):
    """저장된 프리셋 이름들을 순서대로 재생"""
    presets = load_presets()
    for name in names:
        if name not in presets:
            print(f"경고: '{name}' 프리셋이 없습니다. 건너뜁니다")
            continue
        p = presets[name]
        print(f"적용: {name} -> {p}")
        set_led_color(*p["led"])
        motor_ramp(p["direction"], p["speed"])
        time.sleep(pause)
 
# 사용 예
# save_preset("대기", [0, 0, 255], "forward", 0)
# save_preset("경고", [255, 0, 0], "forward", 0)
# save_preset("주행", [0, 255, 0], "forward", 180)
#
# play_sequence(["대기", "경고", "주행", "대기"])

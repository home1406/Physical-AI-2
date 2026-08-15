ZONES = {
    "현관": {"weight": 1.0},
    "창문": {"weight": 1.5},
    "뒷마당": {"weight": 0.8},
}
 
CLASS_SCORE = {"person": 3, "car": 1, "dog": 0.5, "cat": 0.2}
 
def compute_threat_score(zone, detected_class, confidence, is_night):
    zone_weight = ZONES.get(zone, {}).get("weight", 1.0)
    class_score = CLASS_SCORE.get(detected_class, 0.1)
    night_multiplier = 1.5 if is_night else 1.0
    return zone_weight * class_score * confidence * night_multiplier
 
def classify_alert_level(score):
    if score >= 3.0:
        return "CRITICAL"
    elif score >= 1.5:
        return "WARNING"
    elif score >= 0.5:
        return "INFO"
    return "IGNORE"
 
detections = [
    ("창문", "person", 0.92, True),
    ("뒷마당", "cat", 0.75, False),
    ("현관", "car", 0.60, False),
]
for zone, cls, conf, night in detections:
    score = compute_threat_score(zone, cls, conf, night)
    level = classify_alert_level(score)
    print(f"[{level:8s}] {zone} - {cls} (신뢰도 {conf:.0%}, 점수 {score:.2f})")

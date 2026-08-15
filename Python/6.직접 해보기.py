import math
 
class SimpleTracker:
    """중심 좌표 거리 기반의 최소 구현 추적기"""
    def __init__(self, max_distance=60, max_missing=10):
        self.next_id = 0
        self.objects = {}       # id -> (cx, cy)
        self.missing = {}       # id -> 연속 미검출 프레임 수
        self.max_distance = max_distance
        self.max_missing = max_missing
 
    def update(self, detections):
        """detections: [(cx, cy), ...] 이번 프레임의 중심 좌표 목록"""
        assigned = {}
        used = set()
        for oid, (ox, oy) in self.objects.items():
            best, best_dist = None, self.max_distance
            for i, (cx, cy) in enumerate(detections):
                if i in used:
                    continue
                dist = math.hypot(cx - ox, cy - oy)
                if dist < best_dist:
                    best, best_dist = i, dist
            if best is not None:
                assigned[oid] = detections[best]
                used.add(best)
                self.missing[oid] = 0
            else:
                self.missing[oid] = self.missing.get(oid, 0) + 1
 
        for i, det in enumerate(detections):
            if i not in used:
                assigned[self.next_id] = det
                self.missing[self.next_id] = 0
                self.next_id += 1
 
        self.objects = {oid: pos for oid, pos in assigned.items()
                         if self.missing.get(oid, 0) <= self.max_missing}
        return self.objects
 
tracker = SimpleTracker()
# 매 프레임: centers = [(cx1,cy1), (cx2,cy2), ...]
# tracked = tracker.update(centers)
# for oid, (cx, cy) in tracked.items(): draw ID at (cx, cy)

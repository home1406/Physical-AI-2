import cv2, numpy as np, time

class LaneDetector:
    WHITE_LOWER = np.array([  0,   0, 200])
    WHITE_UPPER = np.array([180,  60, 255])

    def __init__(self, frame_w=320, frame_h=240):
        self.frame_w  = frame_w
        self.frame_h  = frame_h
        self.center_x = frame_w // 2

    def detect(self, frame_rgb):
        roi_start = self.frame_h * 40 // 100
        roi  = frame_rgb[roi_start:, :]
        hsv  = cv2.cvtColor(roi, cv2.COLOR_RGB2HSV)
        mask = cv2.inRange(hsv, self.WHITE_LOWER, self.WHITE_UPPER)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
        mask   = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  kernel)
        mask   = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        M = cv2.moments(mask)
        if M["m00"] == 0: return None, 0
        cx    = int(M["m10"] / M["m00"])
        error = cx - self.center_x
        return cx, error

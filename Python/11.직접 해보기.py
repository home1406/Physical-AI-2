import math
 
def estimate_lane_angle(near_x, far_x, near_y=400, far_y=200):
    """두 높이에서의 차선 x좌표로 진행 방향 대비 기울기(도) 추정"""
    dx = far_x - near_x
    dy = near_y - far_y  # 화면 좌표는 아래로 갈수록 y가 커짐
    angle_rad = math.atan2(dx, dy)
    return math.degrees(angle_rad)
 
def combined_steering(center_error, lane_angle, kp_pos=0.4, kp_angle=0.6):
    """위치 오차와 각도 오차를 함께 반영한 조향값 계산"""
    return kp_pos * center_error + kp_angle * lane_angle
 
# 사용 예: 11.1절의 차선 인식 함수에서 두 높이의 차선 중심을 각각 구했다고 가정
near_center_x, far_center_x = 330, 300  # 예시 값
angle = estimate_lane_angle(near_center_x, far_center_x)
steer = combined_steering(center_error=330-320, lane_angle=angle)
print(f"추정 차선 각도: {angle:.1f}도, 최종 조향값: {steer:.2f}")

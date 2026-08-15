import time
 
def avoid_obstacle(car, dist_front, dist_left, dist_right,
                    stop_dist=20, slow_dist=40):
    """전방 장애물 감지 시 좌우 중 더 여유 있는 방향으로 회피"""
    if dist_front is None or dist_front > slow_dist:
        return "직진"
 
    if dist_front < stop_dist:
        car.stop()
        left_ok = dist_left is None or dist_left > stop_dist
        right_ok = dist_right is None or dist_right > stop_dist
 
        if left_ok and (not right_ok or (dist_left or 0) >= (dist_right or 0)):
            car.turn_left(speed=60)
            action = "좌회전 우회"
        elif right_ok:
            car.turn_right(speed=60)
            action = "우회전 우회"
        else:
            car.backward(speed=50)
            action = "후진 (양쪽 모두 막힘)"
        time.sleep(0.4)
        car.stop()
        return action
    else:
        car.forward(speed=40)  # 감속 주행
        return "감속 직진"
 
# 메인 루프 예시
# while True:
#     d_front = measure_distance(TRIG_F, ECHO_F)
#     d_left  = measure_distance(TRIG_L, ECHO_L)
#     d_right = measure_distance(TRIG_R, ECHO_R)
#     action = avoid_obstacle(car, d_front, d_left, d_right)
#     print(action)

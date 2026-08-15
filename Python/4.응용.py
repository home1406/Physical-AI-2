import cv2
import cv2.aruco as aruco
 
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)
aruco_params = aruco.DetectorParameters()
detector = aruco.ArucoDetector(aruco_dict, aruco_params)
 
cap = cv2.VideoCapture(0)
 
while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    corners, ids, _ = detector.detectMarkers(gray)
 
    if ids is not None:
        aruco.drawDetectedMarkers(frame, corners, ids)
        for corner, marker_id in zip(corners, ids.flatten()):
            pts = corner[0]
            cx = int(pts[:, 0].mean())
            cy = int(pts[:, 1].mean())
            cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
            cv2.putText(frame, f"ID:{marker_id} ({cx},{cy})",
                        (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX,
                        0.6, (0, 255, 0), 2)
 
    cv2.imshow("ArUco Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
 
cap.release()
cv2.destroyAllWindows()

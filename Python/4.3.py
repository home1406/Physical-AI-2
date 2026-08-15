import cv2, numpy as np

img  = cv2.imread("test.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 트랙바로 실시간 Canny 조절
cv2.namedWindow("Canny Edge", cv2.WINDOW_NORMAL)
cv2.createTrackbar("Threshold 1", "Canny Edge",  50, 500, lambda x: None)
cv2.createTrackbar("Threshold 2", "Canny Edge", 150, 500, lambda x: None)
cv2.createTrackbar("Blur",        "Canny Edge",   3,  15, lambda x: None)

while True:
    t1   = cv2.getTrackbarPos("Threshold 1", "Canny Edge")
    t2   = cv2.getTrackbarPos("Threshold 2", "Canny Edge")
    blur = cv2.getTrackbarPos("Blur",        "Canny Edge")

    blur = blur if blur % 2 == 1 else blur + 1
    blur = max(blur, 1)

    blurred = cv2.GaussianBlur(gray, (blur, blur), 0)
    edges   = cv2.Canny(blurred, t1, t2)

    edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    display = np.hstack([img, edges_color])
    cv2.putText(display, f"T1:{t1} T2:{t2} Blur:{blur}",
                (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    cv2.imshow("Canny Edge", display)

    if cv2.waitKey(1) & 0xFF == ord("q"): break

cv2.destroyAllWindows()

import cv2
import numpy as np
import random

cap = cv2.VideoCapture(0)

bubble_x, bubble_y = 300,200
bubble_x2, bubble_y2 = 600,300
radius = 45
score = 0
prev_gray = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if prev_gray is not None:
        frame_diff = cv2.absdiff(prev_gray, gray)
        _, thresh = cv2.threshold(frame_diff, 25, 255, cv2.THRESH_BINARY)


        y1, y2 = max(0, bubble_y - radius), min(h, bubble_y + radius)
        x1, x2 = max(0, bubble_x - radius), min(w, bubble_x + radius)
        y3, y4 = max(0, bubble_y2- radius), min(h, bubble_y2 + radius)
        x3, x4 = max(0, bubble_x2 - radius), min(w, bubble_x2 + radius)
        bubble_roi = thresh[y1:y2, x1:x2]
        bubble_roi2 = thresh[y3:y4, x3:x4]

        if np.count_nonzero(bubble_roi) > 400:
            score += 1
            bubble_x = random.randint(radius + 20, w - radius -20)
            bubble_y = random.randint(radius + 20, h - radius - 20)

        if np.count_nonzero(bubble_roi2) > 400:
            score += 1
            bubble_x2 = random.randint(radius + 20, w - radius -20)
            bubble_y2 = random.randint(radius + 20, h - radius - 20)

    prev_gray = gray

    cv2.circle(frame, (bubble_x, bubble_y), radius, (0,255,0), -1)
    cv2.circle(frame, (bubble_x, bubble_y), radius, (0,0,0), 4)
    cv2.circle(frame, (bubble_x - 12, bubble_y- 12), 8, (50,205,50), -1)

    cv2.circle(frame, (bubble_x2, bubble_y2), radius, (0,0,128,), -1)
    cv2.circle(frame, (bubble_x2, bubble_y2), radius, (0,0,255), 4)
    cv2.circle(frame,(bubble_x2 - 12, bubble_y2 -12 ), 8 ,(255,255,255), -1)


    cv2.putText(frame, f"POPPED: {score}", (30,70),
            cv2.FONT_HERSHEY_COMPLEX, 1.6, (0,255,0), 3)

    cv2.imshow("Pop the bubble", frame)

    if cv2.waitKey(1) == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
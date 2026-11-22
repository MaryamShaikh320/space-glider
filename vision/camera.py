import cv2
from tracking import PoseTracker

cap = cv2.VideoCapture(0)
window_name = "Webcam Feed"

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()  # noqa: PLR1722

poseTracker = PoseTracker()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Cannot recieve frame")
        break

    tracking_frame, torso_center_x = poseTracker.process_frame(frame)

    mirrored_tracking_frame = cv2.flip(tracking_frame, 1)

    cv2.imshow(window_name, mirrored_tracking_frame)

    cv2.waitKey(1)
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
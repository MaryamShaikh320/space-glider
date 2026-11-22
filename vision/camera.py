import cv2
from movement import Movement
from tracking import PoseTracker

cap = cv2.VideoCapture(0)
window_name = "Webcam Feed"

if not cap.isOpened():
    print("Error: Could not open webcam")
    exit()  # noqa: PLR1722

poseTracker = PoseTracker()
movement = Movement()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Cannot recieve frame")
        break

    frame = cv2.flip(frame, 1)

    tracking_frame, torso_x, torso_y = poseTracker.process_frame(frame, frame.shape[:2])

    if torso_x is not None and torso_y is not None:
        # print("torso x: ", torso_x)
        # print("torso y: ", torso_y)

        movement.update(tracking_frame, torso_x, torso_y)
        movement.draw_torso_circle()

    cv2.imshow(window_name, tracking_frame)

    cv2.waitKey(1)
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
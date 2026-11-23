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

    height, width = frame.shape[:2]

    overlay = frame.copy()

    tracking_frame, norm_torso_x, norm_torso_y, torso_x, torso_y = poseTracker.process_frame(frame, frame.shape[:2])

    if torso_x is not None and torso_y is not None:
        # print("torso x: ", torso_x)
        # print("torso y: ", torso_y)

        movement.update(tracking_frame, norm_torso_x, norm_torso_y, torso_x, torso_y)
        movement.draw_torso_circle()
        movement.get_lane()
        print(movement.get_lane())

    cv2.rectangle(overlay, (0, 0), (int(0.33 * width), height), (204, 123, 16), -1)
    cv2.rectangle(overlay, (int(0.33 * width), 0), (int(0.67 * width), height), (64, 125, 50), -1)
    cv2.rectangle(overlay, (int(0.67 * width), 0), (width, height), (54, 65, 122), -1)
    cv2.addWeighted(overlay, 0.3, tracking_frame, 1 - 0.3, 0, tracking_frame)

    cv2.imshow(window_name, tracking_frame)

    cv2.waitKey(1)
    if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
import cv2


def get_camera_lane(cap, pose_tracker, movement):
    ret, frame = cap.read()

    if not ret:
        print("Error: Cannot recieve frame")
        return None, None  # noqa: RET501

    frame = cv2.flip(frame, 1)

    height, width = frame.shape[:2]

    overlay = frame.copy()
    

    tracking_frame, norm_torso_x, norm_torso_y, torso_x, torso_y = pose_tracker.process_frame(frame, frame.shape[:2])

    if torso_x is not None and torso_y is not None:
        # print("torso x: ", torso_x)
        # print("torso y: ", torso_y)

        movement.update(tracking_frame, norm_torso_x, norm_torso_y, torso_x, torso_y)
        movement.draw_torso_circle()

        cv2.rectangle(overlay, (0, 0), (int(0.33 * width), height), (204, 123, 16), -1)
        cv2.rectangle(overlay, (int(0.33 * width), 0), (int(0.67 * width), height), (64, 125, 50), -1)
        cv2.rectangle(overlay, (int(0.67 * width), 0), (width, height), (54, 65, 122), -1)
        cv2.addWeighted(overlay, 0.3, tracking_frame, 1 - 0.3, 0, tracking_frame)

        return movement.get_lane(), tracking_frame

    return None, tracking_frame
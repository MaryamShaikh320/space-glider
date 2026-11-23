import platform
import threading

import cv2

from vision.camera import get_camera_lane
from vision.movement import Movement
from vision.tracking import PoseTracker


class CameraWorker:
    def __init__(self):
        self._stop_event = threading.Event()
        self._lock = threading.Lock()

        self._latest_lane = 1
        self._latest_frame = None

        self._thread = threading.Thread(
            target=self._run,
            daemon=True
        )

    def start(self):
        self._thread.start()

    def get_lane(self):
        with self._lock:
            return self._latest_lane

    def get_frame(self):
        with self._lock:
            if self._latest_frame is None:
                return None
            return self._latest_frame.copy()
    
    def stop(self):
        self._stop_event.set()
        self._thread.join()

    def _run(self):
        print("Camera thread started")


        os_name = platform.system()
        os_backends = {
            "Windows": [cv2.CAP_DSHOW, cv2.CAP_MSMF],
            "Darwin":  [cv2.CAP_AVFOUNDATION],
            "Linux":   [cv2.CAP_V4L2],
        }

        backends = os_backends.get(os_name, []) + [cv2.CAP_ANY]
        for backend in backends:
            cap = cv2.VideoCapture(0, backend)
            if cap.isOpened():
                break
            
        print("camera opened: ", cap.isOpened(), flush=True)
        # cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        # cap.set(cv2.CAP_PROP_FPS, 30)
        
        if not cap.isOpened():
            print("Error: Could not open webcam")
            cap.release()
            return

        pose_tracker = PoseTracker()
        movement = Movement()
        

        try:
            while not self._stop_event.is_set():
                lane, camera_frame = get_camera_lane(
                    cap, pose_tracker, movement
                )

                with self._lock:
                    if lane is not None:
                        self._latest_lane = lane

                    if camera_frame is not None:
                        self._latest_frame = camera_frame

        finally:
            cap.release()
            pose_tracker.pose_landmarker.close()
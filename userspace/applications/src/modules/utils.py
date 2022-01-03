import pickle
import time

import cv2
from src.utils.global_instances import rc


def open_webcam():
    """Simple webcam program with opencv"""

    p = rc.redis_instance.pubsub(ignore_subscribe_messages=True)
    p.subscribe("device-data-realsense")

    while True:
        message = p.get_message()
        if not message:
            time.sleep(0.001)  # be nice to the system :)
            continue

        frame = pickle.loads(message["data"])

        cv2.imshow("Input", frame)

        c = cv2.waitKey(1)
        if c == 27:
            cv2.destroyAllWindows()
            break


if __name__ == "__main__":
    open_webcam("/dev/video1")

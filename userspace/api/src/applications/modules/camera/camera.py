import pickle
import time

import cv2
from src.utils.global_instances import rc


def show_camera(camera_feed: str):
    """Get frames from redis and show them in a window."""

    p = rc.redis_instance.pubsub(ignore_subscribe_messages=True)
    p.subscribe(camera_feed)

    while True:
        message = p.get_message()
        if not message:
            time.sleep(0.001)
            continue

        frame = pickle.loads(message["data"])

        cv2.imshow("Camera feed", frame)

        c = cv2.waitKey(1)
        if c == 27:
            cv2.destroyAllWindows()
            break

import pickle
import time

import cv2
from src.utils.global_instances import rc

WIN_NAME = "Camera feed"


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

        cv2.imshow(WIN_NAME, frame)

        c = cv2.waitKey(1)
        if (
            c == 27 or cv2.getWindowProperty(WIN_NAME, cv2.WND_PROP_VISIBLE) < 1
        ):  # if ESCAPE is pressed or window is closed
            cv2.destroyAllWindows()
            break

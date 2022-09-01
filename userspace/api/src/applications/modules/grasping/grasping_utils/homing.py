import queue
import threading
import time
from typing import List

from libalfred import AlfredAPI

from . import geometry as geom
from . import grasping
from .detection import DetectFlag


class HomingThread(threading.Thread):

    arm: AlfredAPI

    pred_queue: queue.Queue  # queue for getting predictions
    flag: threading.Event  # flag to determine if homing should run or not

    def __init__(
        self,
        arm: AlfredAPI,
        *args,
        detect_flag: DetectFlag,
        img_size: List[int] = [640, 480],
        **kwargs
    ):
        super().__init__(*args, **kwargs)

        self.arm = arm

        self.detect_flag = detect_flag
        self.img_size = img_size

        self.pred_queue = queue.Queue()
        self.flag = threading.Event()

        self.img_center_xy = [self.img_size[0] / 2.0, self.img_size[1] / 2.0]

        self.center_camera_count = 0  # frame skipper


    def run(self):
        pred = self.pred_queue.get()
        task_pending = True

        while True:
            try:
                pred = self.pred_queue.get_nowait()
                task_pending = True
            except queue.Empty:
                pass

            self.handle_pred(pred)

            if task_pending:
                self.pred_queue.task_done()
                task_pending = False

            time.sleep(0.01)

    def handle_pred(self, pred):
        if not self.flag.is_set():
            return

        for _, det in enumerate(pred):  # per image
                for *xyxy, _, cls in reversed(det):
                    if not cls == self.detect_flag.target_id:
                        continue

                    xyxy_list = [coord.item() for coord in xyxy]
                    box_center_xy = geom.get_xyxy_center_point(xyxy_list)

                    # print(box_center_xy, " / ", img_center_xy)
                    xy_diff = geom.xy_diff(box_center_xy, self.img_center_xy)
                    xy_softequals = geom.xy_softequals(
                        box_center_xy, self.img_center_xy, 1.0
                    )
                    if xy_softequals:
                        grasping.grasp()
                    else:
                        self.center_camera_count += 1
                        if self.center_camera_count > 14:
                            print("homing")
                            # print(xy_diff)
                            self.center_camera(xy_diff)
                            self.center_camera_count = 0

                    return


    def center_camera(self, xy_diff):
        """Move arm end effector to center of object."""

        j1 = -(xy_diff[0] / 50.0)
        j5 = xy_diff[1] / 50.0
        # print(f"{j5=}")

        _ = self.arm.set_servo_angle(servo_id=1, angle=j1, relative=True)
        _ = self.arm.set_servo_angle(servo_id=5, angle=j5, relative=True)
        # ret = arm.set_position(x=1, speed=100, mvacc=1000, relative=True)
        # print(f"{ret=}")

import threading
from collections import deque
from dataclasses import dataclass, field
from typing import Dict, List

import torch
from libalfred import AlfredAPI

from . import geometry as geom
from .detection import DetectFlag
from .scanner import ScannerThread

lock = threading.Lock()


@dataclass
class DetectionBuffer:
    """Buffer for specific item detection."""

    name: str
    id: int
    buffer_len: int = 60
    confidence: float = 0.90
    buffer: deque = field(init=False)

    def __post_init__(self):
        self.buffer = deque([-1] * self.buffer_len, maxlen=self.buffer_len)

    def __bool__(self):
        """Returns True if buffer is filled with values, i.e.
        an object was on the frame for maxlen frames."""

        no_detect = 0

        for x in self.buffer:
            if not isinstance(x, torch.Tensor):
                no_detect += 1

        if no_detect > self.confidence * self.buffer_len:
            return False

        return True

    def appendleft(self, value):
        """Append left value to buffer."""

        self.buffer.appendleft(value)

    def updateleft(self, value):
        """Update left value of buffer."""

        self.buffer[0] = value

    def reset(self):
        """Reset buffer."""

        for _ in range(len(self.buffer)):
            self.buffer.appendleft(-1)


_detection_buffers: Dict[int, DetectionBuffer] = {}


def center_camera(arm: AlfredAPI, xy_diff):
    """Move arm end effector to center of object."""

    j1 = -(xy_diff[0] / 50.0)
    j5 = xy_diff[1] / 50.0
    # print(f"{j5=}")

    _ = arm.set_servo_angle(servo_id=1, angle=j1, relative=True)
    _ = arm.set_servo_angle(servo_id=5, angle=j5, relative=True)
    # ret = arm.set_position(x=1, speed=100, mvacc=1000, relative=True)
    # print(f"{ret=}")


def _preds_postprocessor(
    img_size, names, detect_flag: DetectFlag, arm: AlfredAPI
):
    detect_id = [0]
    center_camera_count = [100_000]

    for i, name in enumerate(names):
        _detection_buffers[i] = DetectionBuffer(name, i)
    # print(f"{_detection_buffers=}")

    img_center_xy = [img_size[0] / 2.0, img_size[1] / 2.0]

    scanner_flag = threading.Event()
    # print(scanner_flag, scanner_flag.is_set())
    scanner_execute_return_sequence = threading.Event()
    scanner_thread = ScannerThread(
        arm,
        scanner_flag,
        scanner_execute_return_sequence,
        -130.0,
        100.0,
        daemon=True,
    )
    scanner_thread.start()

    def preds_postprocessor_inner(pred: List[torch.Tensor]):

        # if the arm is resetting its position, skip
        if scanner_execute_return_sequence.is_set():
            return

        # skip if no target was set
        if detect_flag.target_id == -1:
            return

        # add new default detection
        for buffer in _detection_buffers.values():
            buffer.appendleft(-1)

        # add detections to each detected class' buffer
        if any(len(x) != 0 for x in pred):
            for _, det in enumerate(pred):  # per image
                for *xyxy, _, cls in reversed(det):
                    cls = int(cls)
                    # print(f"pred: {det}\ncls: {names[cls]}")
                    _detection_buffers[cls].updateleft(det)

        # if target item was not detected yet,
        # check if it is detected now
        if not detect_flag:
            detection_buffer = _detection_buffers[detect_flag.target_id]

            if detection_buffer:
                print(
                    f"{detect_id[0]} - FOUND! {detect_flag.target_name}",
                    end="\n----------\n",
                )
                detect_id[0] += 1

                detect_flag.set()
                scanner_flag.set()

            return

        if scanner_flag.is_set():
            for _, det in enumerate(pred):  # per image
                for *xyxy, _, cls in reversed(det):
                    if not cls == detect_flag.target_id:
                        continue

                    xyxy_list = [coord.item() for coord in xyxy]
                    box_center_xy = geom.get_xyxy_center_point(xyxy_list)

                    # print(box_center_xy, " / ", img_center_xy)
                    xy_diff = geom.xy_diff(box_center_xy, img_center_xy)
                    # xy_softequals = geom.xy_softequals(
                    #     box_center_xy, img_center_xy, 1.0
                    # )

                    center_camera_count[0] += 1
                    if center_camera_count[0] > 14:
                        print("homing")
                        # print(xy_diff)
                        center_camera(arm, xy_diff)
                        center_camera_count[0] = 0

                    return

        # if flag was set but target was not found

        _detection_buffers[detect_flag.target_id].reset()
        detect_flag.unset()
        print("lost object")

        scanner_execute_return_sequence.set()
        scanner_flag.clear()

    return preds_postprocessor_inner

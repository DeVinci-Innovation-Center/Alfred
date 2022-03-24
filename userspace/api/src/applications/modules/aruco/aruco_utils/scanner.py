import math
import numpy as np
import threading
import time

from itertools import cycle
from libalfred import AlfredAPI


lock = threading.Lock()


# base time + time added by num_points + pause between angles
def time_to_move(x): return 0.2 + 10.0 / x - (x - 10) / 7 + 0.5


# TODO: exploration / tracking coefficients: moves faster when exploration is high, looks for item for longer if high
# TODO: detect object movement with position gradient; explore direction where object has gone when it disappears


class ScannerThread(threading.Thread):
    """Thread to scan the environment with xArm"""
    arm: AlfredAPI

    flag: threading.Event
    execute_return_sequence: threading.Event

    loop: cycle

    start_pose_degrees: list = [0.0, -42.3, -71.5, 0.0, 91.0, 0.0]

    def __init__(
        self,
        arm: AlfredAPI,
        min_angle: float,
        max_angle: float,
        num_points: int = 10,
        daemon: bool = True,
    ):
        super().__init__(daemon=daemon)

        self.arm = arm

        self.num_points = num_points
        self.flag = threading.Event()  # execution flag; stops execution when True
        self._stop = threading.Event()

        min_to_max_pass_points = np.linspace(min_angle, max_angle, num_points)
        self.loop = cycle(
            list(min_to_max_pass_points[1:-1]) +
            list(min_to_max_pass_points[::-1])
        )

        for i in range(math.floor((self.num_points * 2 - 2) * 3 / 4)):
            next(self.loop)

    def run(self) -> None:
        """Move xArm while scanning the environment"""

        self.start_sequence()
        while True:
            if self.flag.is_set():
                time.sleep(0.1)
                continue

            if self._stop.is_set():
                self.return_sequence()
                break

            point = next(self.loop)
            self.arm.set_servo_angle(
                servo_id=1, angle=point, is_radian=False, wait=False
            )
            time.sleep(time_to_move(self.num_points))

    def start_sequence(self):
        """Gets xArm into init_position."""

        self.flag.set()
        print("Getting into position!")
        self.arm.set_servo_angle(
            angle=self.start_pose_degrees, is_radian=False, wait=True)
        print("Got into position!")
        self.flag.clear()

    def return_sequence(self):
        """Gets xArm back into init_position after stop flag was set."""
        self.flag.set()
        print("Executing return sequence!")
        self.arm.set_servo_angle(
            angle=self.start_pose_degrees, is_radian=False, wait=True)
        print("Finished return sequence")
        self.flag.clear()

    def set(self, validate=True):
        self.flag.set()

    def unset(self):
        self.flag.clear()

    def stop(self):
        """Stop the thread"""
        self._stop.set()

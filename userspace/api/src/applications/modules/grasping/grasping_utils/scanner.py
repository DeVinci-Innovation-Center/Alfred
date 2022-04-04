import math
import threading
import time
from itertools import cycle

import numpy as np
from libalfred import AlfredAPI

lock = threading.Lock()


time_to_move = lambda x: 0.2 + 10.0 / x - (x - 10) / 7 + 0.5 # base time + time added by num_points + pause between angles


# TODO: exploration / tracking coefficients: moves faster when exploration is high, looks for item for longer if high
# TODO: detect object movement with position gradient; explore direction where object has gone when it disappears


class ScannerThread(threading.Thread):

    arm: AlfredAPI

    flag: threading.Event
    execute_return_sequence: threading.Event

    loop: cycle

    start_pose_degrees: list = [0.0, -42.3, -71.5, 0.0, 91.0, 0.0]

    def __init__(
        self,
        arm: AlfredAPI,
        flag: threading.Event,
        execute_return_sequence: threading.Event,
        min_angle: float,
        max_angle: float,
        num_points: int = 10,
        daemon: bool = True,
    ):
        super().__init__(daemon=daemon)

        self.arm = arm

        self.num_points = num_points
        self.flag = flag  # execution flag; stops execution when True
        self.execute_return_sequence = execute_return_sequence

        min_to_max_pass_points = np.linspace(min_angle, max_angle, num_points)
        self.loop = cycle(
            list(min_to_max_pass_points[1:-1]) + list(min_to_max_pass_points[::-1])
        )

        for i in range(math.floor((self.num_points * 2 - 2) * 3 / 4)):
            next(self.loop)

    def run(self):

        self.start_sequence()

        while True:
            if self.flag.is_set():
                time.sleep(0.1)
                continue

            if self.execute_return_sequence.is_set():
                self.return_sequence()
                continue

            point = next(self.loop)
            self.arm.set_servo_angle(
                servo_id=1, angle=point, is_radian=False, wait=False
            )
            time.sleep(time_to_move(self.num_points))

    def start_sequence(self):
        """Gets xArm into position."""

        # Execute start sequence
        self.flag.set()
        print("Getting into position!")

        for i, angle in enumerate(self.start_pose_degrees[:-1]):
            servo_id = i + 1
            self.arm.set_servo_angle(servo_id=servo_id, angle=angle)

        self.arm.set_servo_angle(
            servo_id=len(self.start_pose_degrees),
            angle=self.start_pose_degrees[-1],
            wait=True,
        )

        print("Got into position!")

        self.flag.clear()

    def return_sequence(self):
        """Gets xArm back into position after stop flag was set."""

        # Execute return sequence
        print("Executing return sequence!")

        for i, angle in enumerate(self.start_pose_degrees[1:-1]):
            servo_id = i + 2
            self.arm.set_servo_angle(servo_id=servo_id, angle=angle)

        self.arm.set_servo_angle(
            servo_id=len(self.start_pose_degrees),
            angle=self.start_pose_degrees[-1],
            wait=True,
        )

        print("Finished return sequence")
        self.execute_return_sequence.clear()
        self.flag.clear()

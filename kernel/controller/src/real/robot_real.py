import time

from xarm.wrapper import XArmAPI


class RobotReal(XArmAPI):
    """Class for real xArm, custom to our needs."""

    def __init__(self, ip: str):
        super().__init__(port=ip, do_not_open=True)

    def connect_loop(self):
        """Try to connect indefinitely, with a pause of 3 seconds
        between tries."""
        connected = False
        while not connected:
            try:
                self.connect()
                connected = True
            except Exception:  # pylint: disable = broad-except
                print("arm is not online. trying again in 3 seconds...")
                time.sleep(3)

        self.motion_enable(enable=True)
        self.set_mode(0)
        self.set_state(state=0)
        # self.set_world_offset([0] * self.axis)

        time.sleep(1)

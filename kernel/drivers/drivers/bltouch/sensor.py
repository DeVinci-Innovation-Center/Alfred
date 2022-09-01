import time

from serial import Serial


class BLTouch:
    def __init__(
        self, port: str = "/dev/ttyACM1", baudrate: int = 9600, timeout: int = 0.1
    ) -> None:
        self.ser = Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.port = port
        self.baudrate = baudrate
        self.data = ""
        time.sleep(2)  # waiting to initialize the serial communication

    def send_command(self, command: str = "1") -> None:
        """
        command:str default="1" -> activate the leveling sensor
        if command="2" -> activate only the Pull-pin Up
        """
        self.ser.write(bytes(command, "utf-8"))
        time.sleep(0.5)

    def get_data(self) -> str:
        self.data = self.ser.readline().decode(
            "utf"
        )  # if nothing on serial is detected, after "timeout" seconds, it returns: ""
        return self.data

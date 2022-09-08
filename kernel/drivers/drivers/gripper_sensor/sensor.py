import time

from serial import Serial


class FSR:
    def __init__(self, port: str = "/dev/ttyACM1", baudrate: int = 9600, timeout: int = 0.05) -> None:
        self.ser = Serial(port=port, baudrate=baudrate, timeout=timeout)
        self.port = port
        self.baudrate = baudrate
        self.data = ""
        time.sleep(2) # waiting to initialize the serial communication

    def send_command(self,command:str="2")->None:
        """
        command:str default="2" -> activate the leveling sensor, the second time stop the stream
        """
        self.ser.write(bytes(command, 'utf-8'))
        time.sleep(0.5)

    def get_data(self) -> str:
        self.data = self.ser.readline().decode("utf") # if nothing on serial is detected, after "timeout" seconds, it returns: ""
        return self.data

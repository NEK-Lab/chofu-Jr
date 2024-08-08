import serial
import time
from setting import serial_setting
from controller import logicool_controller

serial_const = serial_setting()
controller = logicool_controller()

class serial_communicator:
    def __init__(self):
        self.open()
        self.data = [0]*20

    def open(self):
        i = 0
        while i != -1:
            try:
                self.serial_port = serial.Serial(serial_const.port[i], serial_const.speed, timeout=serial_const.timeout)
                i = -1
            except Exception as e:
                i = i+1

    def communicate(self):
        self.data = controller.check_state()  # Call the method correctly

        if self.data is None:
            return

        if not isinstance(self.data, list):
            return

        # Ensure data values are within the range 0-255

        # Convert the list to a comma-separated string
        data_str = ','.join(map(str, self.data)) + '\n'

        try:
            # Encode the string to bytes and send it to the Arduino
            self.serial_port.write(data_str.encode())
            print("Sent:", data_str.encode())
        except Exception as e:
            print("Error sending data:", e)

    def read_from_arduino(self):
        if self.serial_port.in_waiting > 0:
            received_data = self.serial_port.read(self.serial_port.in_waiting)
            print("Received:", received_data.decode().strip())
            # Process received data as needed

    def close(self):
        if self.serial_port.is_open:
            self.serial_port.close()
            print("Serial port closed")

if __name__ == '__main__':
    app = serial_communicator()
    try:
        while True:
            app.communicate()
            app.read_from_arduino()
            time.sleep(0.01)  # Add a delay to avoid overwhelming the serial port
    except KeyboardInterrupt:
        print("Program interrupted by user")
    finally:
        app.close()

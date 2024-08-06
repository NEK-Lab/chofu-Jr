import serial
from setting import serial_setting
from controller import logicool_controller

serial_const = serial_setting()
controller = logicool_controller()

class serial_communicater:
    def __init__(self):
        self.serial_port = serial.Serial(serial_const.port, serial_const.speed, timeout=serial_const.timeout)
        self.data = [0]*19

    def communicate(self):
        self.data = controller.check_state

        data_to_send = ",".join(map(str, self.data))
        self.serial_port.write(data_to_send.encode())
        #print(data_to_send.encodserial.serialutil.serialtimeoutexception: Write timeoute())

if __name__ == '__main__':
    app = serial_communicater()    
    while True:
        app.communicate()

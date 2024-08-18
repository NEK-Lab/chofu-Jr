from setting import serial_setting
from controller import logicool_controller
from kanicam import webcamcapture
from gui import Application, SerialCommunicator

def main():
    serial_const = serial_setting()
    controller = logicool_controller()
    kanicam = webcamcapture()
    
    serial_comm = SerialCommunicator(serial_const, controller)
    app = Application(serial_comm, kanicam)
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()

if __name__ == "__main__":
    main()

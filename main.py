import pygame
import serial

class PS4ControllerGUI:
    def __init__(self):
        pygame.init()
        self.ps4 = pygame.joystick.Joystick(0)
        self.ps4.init()
        self.serial_port = serial.Serial("COM5", 9600, timeout=0.1)
        self.result = '5'

    def read_joystick(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.JOYBUTTONDOWN:
                if self.ps4.get_button(0):
                    print("Pressed Cross")
                    self.result = '2'
                elif self.ps4.get_button(1):
                    print("Pressed Circle")
                    self.result = '4'
                elif self.ps4.get_button(2):
                    print("Pressed Square")
                    self.result = '3'
                elif self.ps4.get_button(3):
                    print("Pressed Triangle")
                    self.result = '1'
                elif self.ps4.get_button(4):
                    print("Pressed Share")
                elif self.ps4.get_button(5):
                    print("Pressed PS")
                    pygame.quit()
                elif self.ps4.get_button(6):
                    print("Pressed Options")
                elif self.ps4.get_button(7):
                    print("Pressed L3")
                elif self.ps4.get_button(8):
                    print("Pressed R3")
                elif self.ps4.get_button(9):
                    print("Pressed L1")
                    self.result = '5'
                elif self.ps4.get_button(10):
                    print("Pressed R1")
                elif self.ps4.get_button(11):
                    print("Pressed Up")
                    self.result = '6'
                elif self.ps4.get_button(12):
                    print("Pressed Down")
                    self.result = '7'
                elif self.ps4.get_button(13):
                    print("Pressed Left")
                    self.result = '9'
                elif self.ps4.get_button(14):
                    print("Pressed Right")
                    self.result = '8'
                elif self.ps4.get_button(15):
                    print("Pressed Touchpad")
                    self.result = '5'
            elif event.type == pygame.JOYBUTTONUP:
                print("Released")
                self.result = '5'

        self.serial_port.write(str.encode(self.result))

if __name__ == '__main__':
    chof = PS4ControllerGUI()
    
    while True:
        chof.read_joystick()

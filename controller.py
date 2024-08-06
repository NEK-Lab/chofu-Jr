import pygame
from setting import controller_setting
controller_const = controller_setting()
class logicool_controller:
    def __init__(self):
        pygame.init()
        self.logicool = pygame.joystick.Joystick(0)
        self.logicool.init()
        self.status = [None] * 18

    def check_state(self):
        events = pygame.event.get()
        if events:
            #print(events)
            for i in range(4):
                self.check_axis(i)
            for i in range(12):
                self.check_btn(i)
            self.check_hat()
            #print(self.status)
            formatted_status = [format(x, '>4') for x in self.status]
            print("[" + ", ".join(formatted_status) + "]")
            return self.status

    def check_axis(self,axnum):
        axis_value = int(self.logicool.get_axis(axnum)*256*((-1)**(axnum)))
        if abs(axis_value) > controller_const.joystickmin:
            self.status[axnum] = axis_value
        else:
            self.status[axnum] = 0

    def check_btn(self,btnnum):
        if self.logicool.get_button(btnnum):
            self.status[btnnum+4] = 1
        else:
            self.status[btnnum+4] = 0

    def check_hat(self):
        hat_value = self.logicool.get_hat(0)
        if hat_value != (0, 0):
            self.status[16] = hat_value[0]
            self.status[17] = hat_value[1]
        else:
            self.status[16] = 0
            self.status[17] = 0

if __name__ == '__main__':
    app = logicool_controller()
    while app.status[12] != 1:
        app.check_state()
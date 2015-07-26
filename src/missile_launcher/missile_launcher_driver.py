import platform
import time

import usb.core
import usb.util


class MissileLauncherDriver(object):

    DOWN = "down"
    UP = "up"
    LEFT = "left"
    RIGHT = "right"
    FIRE = "fire"
    STOP = "stop"
    MOVE_TO = "move-to"
    MOVE = "move"
    MOVES = "moves"
    CENTER = "center"
    LED_ON = "led-on"
    LED_OFF = "led-off"

    codes = {
        DOWN: 0x01,
        UP: 0x02,
        LEFT: 0x04,
        RIGHT: 0x08,
        FIRE: 0x10,
        STOP: 0x20,
        LED_ON: 0x01,
        LED_OFF: 0x00
    }

    commands = codes.keys() + [MOVE_TO, MOVE, CENTER]

    missile_capacity = 4
    y_speed = 0.48
    x_speed = 1.2
    x_range = 6.5
    y_range = 0.75

    def __init__(self):
        self.device = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        if self.device is None:
            raise ValueError('Missile device not found')

        if platform.system() == "Linux":
            try:
                self.device.detach_kernel_driver(0)
            except Exception:
                pass

        self.device.set_configuration()
        self.center()

    def execute(self, cmd):
        if cmd in self.codes:
            if cmd.startswith("led"):
                self.device.ctrl_transfer(0x21, 0x09, 0, 0, [
                    0x03, self.codes[cmd],
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00
                ])
            else:
                self.device.ctrl_transfer(0x21, 0x09, 0, 0, [
                    0x02, self.codes[cmd],
                    0x00, 0x00, 0x00, 0x00, 0x00, 0x00
                ])
        elif cmd == self.CENTER:
            self.center()
        elif isinstance(cmd, dict):
            cmd_key = cmd.keys()[0]
            if cmd_key == self.MOVE:
                self.move(
                    cmd[cmd_key]['x_distance'], cmd[cmd_key]['y_distance']
                )
            elif cmd_key == self.MOVE_TO:
                self.move_to(
                    cmd[cmd_key]['x_percentage'], cmd[cmd_key]['y_percentage']
                )
        else:
            raise ValueError('Invalid command')

    def up(self):
        self.execute(self.UP)

    def down(self):
        self.execute(self.DOWN)

    def left(self):
        self.execute(self.LEFT)

    def right(self):
        self.execute(self.RIGHT)

    def stop(self):
        self.execute(self.STOP)

    def fire(self):
        self.execute(self.FIRE)
        time.sleep(3)

    def led_on(self):
        self.execute(self.LED_ON)

    def led_off(self):
        self.execute(self.LED_OFF)

    def center(self, x=0.5, y=0.5):
        self.move_to(x, y)
        self.left()
        time.sleep(self.x_range)
        self.right()
        time.sleep(x * self.x_range)
        self.stop()

        self.up()
        time.sleep(self.y_range)
        self.down()
        time.sleep(y * self.y_range)
        self.stop()

    def move_to(self, x_percentage, y_percentage):
        if (x_percentage > 0):
            self.right()
        elif(x_percentage < 0):
            self.left()
        time.sleep(abs(x_percentage) * self.x_range)
        self.stop()
        if (y_percentage > 0):
            self.down()
        elif(y_percentage < 0):
            self.up()
        time.sleep(abs(y_percentage) * self.y_range)
        self.stop()

    def move(self, x_distance, y_distance):
        x_seconds = x_distance * self.x_speed
        y_seconds = y_distance * self.y_speed

        horizontal = 0
        vertical = 0
        if x_seconds > 0:
            horizontal = self.RIGHT
        elif x_seconds < 0:
            horizontal = self.LEFT

        if y_seconds > 0:
            vertical = self.DOWN
        elif y_seconds < 0:
            vertical = self.UP

        self.execute(vertical | horizontal)

        if (abs(x_seconds) > abs(y_seconds)):
            time.sleep(abs(y_seconds))
            self.execute(horizontal)
            time.sleep(abs(x_seconds - y_seconds))
        else:
            time.sleep(abs(x_seconds))
            self.execute(vertical)
            time.sleep(abs(y_seconds - x_seconds))

        self.stop()

    def dispose(self):
        self.stop()
        self.led_off()

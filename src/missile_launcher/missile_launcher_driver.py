import platform
import usb.core
import usb.util


class MissileLauncherDriver(object):
    commands = {
        "down": 0x01,
        "up": 0x02,
        "left": 0x04,
        "right": 0x08,
        "fire": 0x10,
        "stop": 0x20
    }

    def __init__(self):
        self.setup_device()
        self.device.set_configuration()

    def setup_device(self):
        self.device = usb.core.find(idVendor=0x2123, idProduct=0x1010)
        if self.device is None:
            raise ValueError('Missile device not found')

        if "Linux" == platform.system():
            try:
                self.device.detach_kernel_driver(0)
            except Exception:
                pass

    def send_cmd(self, cmd):
        self.device.ctrl_transfer(
            0x21, 0x09, 0, 0, [0x02, cmd, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]
        )

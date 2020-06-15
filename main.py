import pystray
import serial
from serial.tools import list_ports
import threaded_image_grabber
import framerate_limiter
from PIL import Image


class App:

    BAUD_RATES = [300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400, 57600, 115200]
    FRAME_RATES = [2, 5, 10, 20, 30, 50, 60, 75, 120, 144, 200]

    def __init__(self) -> None:
        self.grabber = threaded_image_grabber.ThreadedImageGrabber()

        self.limiter = framerate_limiter.FramerateLimiter(30)

        self.icon = pystray.Icon("Ambient Lighting", Image.open('icon.png'))

        self.serial = serial.Serial()
        self.serial.baudrate = 9600

        self.update_menu()

    def update_menu(self):
        self.icon.menu = pystray.Menu(
            pystray.MenuItem(
                "Serial Port",
                pystray.Menu(
                    *self.get_serial_port_options()
                ),
                enabled=not self.serial.is_open
            ),

            pystray.MenuItem(
                "Baudrate",
                pystray.Menu(
                    *[pystray.MenuItem(str(i), self.select_baudrate_option(i), checked=self.is_selected_baudrate(i), radio=True) for i in
                      (App.BAUD_RATES)]
                ),
                enabled=not self.serial.is_open
            ),
            pystray.MenuItem(
                "Framerate",
                pystray.Menu(
                    *[pystray.MenuItem(str(i), self.select_framerate_option(i), checked=self.is_selected_framerate(i),
                                       radio=True) for i in
                      (App.FRAME_RATES)]
                )
            ),
            pystray.MenuItem(
                "Start",
                self.start_communication,
                visible=not self.serial.is_open
            ),
            pystray.MenuItem(
                "Stop",
                self.stop_communication,
                visible=self.serial.is_open
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Exit", self.exit_program)
        )

        self.icon.update_menu()

    def get_serial_port_options(self):
        serial_ports = list_ports.comports()
        refresh_button = pystray.MenuItem("Refresh", self.update_menu)
        if len(serial_ports) > 0:
            return [pystray.MenuItem(str(i), self.select_port_option(i), checked=self.is_selected_serial_port(i), radio=True) for i in (serial_ports)] + [pystray.Menu.SEPARATOR, refresh_button]
        else:
            return [pystray.MenuItem("(None)", None, enabled=False), pystray.Menu.SEPARATOR, refresh_button]

    def start_communication(self):
        if self.is_ready_to_start():
            self.serial.open()
            self.update_menu()

    def stop_communication(self):
        self.serial.close()
        self.update_menu()

    def select_baudrate_option(self, value):
        def inner(icon, item):
            self.serial.baudrate = value
        return inner

    def select_port_option(self, value):
        def inner(icon, item):
            self.serial.port = value.device
        return inner

    def select_framerate_option(self, value):
        def inner(icon, item):
            self.limiter.set_new_framerate(value)
        return inner

    def is_selected_framerate(self, value):
        def inner(item):
            return self.limiter.desired_s_per_frame == 1/value
        return inner

    def is_selected_baudrate(self, value):
        def inner(item):
            return self.serial.baudrate == value
        return inner

    def is_selected_serial_port(self, value):
        def inner(item):
            return self.serial.port == value.device
        return inner

    def is_ready_to_start(self):
        conditions = {
            'FPS': self.limiter.current_fps is not None,
            'Baud Rate': self.serial.baudrate is not None,
            'Serial Port':self.serial.port is not None
        }

        ready = all([conditions[i] for i in conditions])

        if not ready:
            self.icon.notify(
                "Could not start serial communication.\n The following need to be configured:\n" + '\n'.join([i for i in conditions if not conditions[i]])
            )

        return ready

    def program_loop(self, icon):
        icon.visible = True

        self.grabber.start()

        while self.grabber.is_running:
            if self.serial.is_open:
                frames = self.grabber.pull_frame_and_request_next()
                self.serial.write(b"Hello\n")
            self.limiter.tick()

    def exit_program(self):
        self.grabber.stop()
        self.stop_communication()
        self.icon.stop()

    def run(self):
        self.icon.run(self.program_loop)


if __name__ == '__main__':
    app = App()
    app.run()

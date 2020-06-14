import pystray
import threaded_image_grabber
import framerate_limiter
from PIL import Image

class App:

    def __init__(self) -> None:
        self.grabber = threaded_image_grabber.ThreadedImageGrabber()

        self.limiter = framerate_limiter.FramerateLimiter(30)

        menu = pystray.Menu(pystray.MenuItem("Button", lambda: print("Click")), pystray.MenuItem("Exit", self.exit_program))
        self.icon = pystray.Icon("Ambient Lighting", Image.open('icon.png'), menu=menu)


    def program_loop(self, icon):
        icon.visible = True

        self.grabber.start()

        while self.grabber.is_running:
            frame = self.grabber.pull_frame_and_request_next()
            # process data and output to serial
            self.limiter.tick()


    def exit_program(self):
        self.grabber.stop()
        self.icon.stop()


    def run(self):
        self.icon.run(self.program_loop)


if __name__ == '__main__':
    app = App()
    app.run()
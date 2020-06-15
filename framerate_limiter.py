import time

class FramerateLimiter:

    def __init__(self, desired_fps) -> None:

        self.desired_s_per_frame = 1/desired_fps # desired_fps to seconds per frame (spf)

        self.last_update = 0
        self.current_fps = 0

    def tick(self):
        time_delta = time.time() - self.last_update
        extra_time = self.desired_s_per_frame - time_delta
        time.sleep(max(extra_time, 0))
        post_sleep_delta = time.time() - self.last_update
        self.last_update = post_sleep_delta + self.last_update
        if post_sleep_delta > 0:
            self.current_fps = 1 / (post_sleep_delta)

    def set_new_framerate(self, value):
        self.desired_s_per_frame = 1/value
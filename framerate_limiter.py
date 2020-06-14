import time

class FramerateLimiter:

    def __init__(self, desired_fps) -> None:

        self.desired_s_per_frame = 1/desired_fps # fps to seconds per frame (spf)

        self.last_update = 0

    def tick(self):
        time_delta = time.time() - self.last_update

        extra_time = self.desired_s_per_frame - time_delta
        time.sleep(max(extra_time, 0))


        self.last_update = time.time()
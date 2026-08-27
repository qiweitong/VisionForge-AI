# camera/fps.py
import time

class FPSCounter:
    def __init__(self):
        self.last_time = time.time()
        self.fps = 0

    def update(self):
        current = time.time()
        self.fps = 1 / (current - self.last_time)
        self.last_time = current
        return self.fps
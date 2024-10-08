from time import gmtime, time
from random import SystemRandom


cryptosecure_random = SystemRandom().randrange


class Clock:
    def __init__(self, region, utc_offset, centrex, centrey) -> None:
        self.region:     str = region
        self.utc_offset: int = utc_offset
        self.centrex:    int = centrex
        self.centrey:    int = centrey

        self.hour:       int
        self.minute:     int
        self.second:     int

        self.hand_second: int

        self.calibrate()

    def calibrate(self) -> None:
        """Get accurate current time."""
        now = gmtime()

        self.hour = (now.tm_hour + self.utc_offset) % 12
        self.minute = now.tm_min
        self.second = now.tm_sec
        if self.second <= 10:
            self.hand_second = cryptosecure_random(0, 59)
            self.precise_second = time() % 1
        elif self.second >= 58:
            self.hand_second = 58
            self.precise_second = 0
        else:
            self.hand_second = self.second
            self.precise_second = time() % 1


class Fake_Clock(Clock):
    def calibrate(self):
        now = gmtime()

        self.hour = (now.tm_hour + self.utc_offset) % 12 * -1
        self.minute = now.tm_min * -1
        self.second = now.tm_sec * -1
        if self.second >= -10:
            self.hand_second = cryptosecure_random(0, 59)
            self.precise_second = time() % 1 * -1
        elif self.second >= 58:
            self.hand_second = 58
            self.precise_second = 0
        else:
            self.hand_second = self.second
            self.precise_second = time() % 1 * -1

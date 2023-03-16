"""
    Time Transformation
"""

import random
import time
from datetime import datetime
from functools import wraps
from typing import Optional, Any, Callable
import pytz

import arrow
from arrow import Arrow


__all__ = (
    "smart_delay",
    "utc_offset",
    "timing",
    "Timer",
)


def smart_delay(seconds: float, demo: bool = False) -> float:
    """Smart delay for seconds of time, demo=True for skip real sleep."""
    small, big = float(seconds * 4 / 5), float(seconds * 6 / 5)
    pause = random.uniform(small, big)
    if not demo:
        time.sleep(pause)
    return pause


def utc_offset(time_zone: str) -> int:
    """Convert time zone string to utc offset integer for hour diff."""
    now = datetime.now(pytz.timezone(time_zone))
    offset = now.utcoffset()
    if offset:
        return int(offset.total_seconds() / 3600)
    return 0


def timing(func: Callable) -> Any:
    """Measure Timing of functions"""

    @wraps(func)
    def wrap(*args: Any, **kwargs: Any) -> Any:
        """Wrap function."""
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(
            "func:%r args:%r, kwargs:%r took: %2.8f sec"
            % (func.__name__, args, kwargs, end - start)
        )

        return result

    return wrap


class Timer:
    """Base cls for time transformation"""

    __slots__ = ("tz_offset", "now", "fmt")

    def __init__(self, tz_offset: int = 8) -> None:
        """Init Timer."""
        self.tz_offset = tz_offset
        self.now = arrow.utcnow().shift(hours=tz_offset)
        self.fmt = "YYYY-MM-DD HH:mm:ss"

    def to_str(self, now: Optional[Arrow] = None, fmt: str = "") -> str:
        """string format for now"""
        fmt = fmt if fmt else self.fmt
        now = now if now else self.now
        return now.format(fmt)

    def to_ts(self, now: Optional[Arrow] = None) -> int:
        """int timestamp for now"""
        now = now if now else self.now
        return int(now.timestamp())

    def ts2str(self, now_ts: int, fmt: str = "") -> str:
        """int to string for timestamp of now"""
        fmt = fmt if fmt else self.fmt
        return arrow.get(now_ts).format(fmt)

    def str2ts(self, now_str: str, fmt: str = "") -> int:
        """string to int for timestamp of now"""
        fmt = fmt if fmt else self.fmt
        return int(arrow.get(now_str, fmt).timestamp())

    def iso_week(self, offset: int = 0) -> str:
        """return ISO week format like: `2020W36`"""
        iso = self.now.shift(weeks=offset).isocalendar()
        return "{}W{}".format(iso[0], iso[1])


class TestTimer:
    """TestCase for Timer."""

    @staticmethod
    def test_smart_delay() -> None:
        """Test smart delay."""
        start = time.time()
        seconds = random.uniform(a=0.0, b=1.0)
        delay = smart_delay(seconds=seconds, demo=True)
        print(f"delay = {delay}")
        small, big = float(seconds * 4 / 5), float(seconds * 6 / 5)
        assert small < delay < big
        end = time.time()
        assert end >= start

        start = time.time()
        seconds = random.uniform(a=0.0, b=1.0)
        delay = smart_delay(seconds=seconds, demo=False)
        print(f"delay = {delay}")
        small, big = float(seconds * 4 / 5), float(seconds * 6 / 5)
        assert small < delay < big
        end = time.time()
        assert end > start

    @staticmethod
    def test_utc_offset() -> None:
        """Test UTC offset"""
        time_zone = "Asia/hong_kong"
        offset = utc_offset(time_zone)
        assert offset == 8

    @staticmethod
    @timing
    def delay(name: str, pause: float) -> float:
        """Delay for pause, return pause."""
        print(f"anme = {name}")
        time.sleep(pause)
        return pause

    def test_timeit(self) -> None:
        """Test timeit."""
        name = "Andy"
        pause = 0.5
        assert pause == self.delay(name, pause=pause)

    @staticmethod
    def test_timer() -> None:
        """Test timer cls."""
        timer = Timer()
        now_ts = timer.to_ts()
        now_str = timer.to_str()
        assert now_ts == timer.str2ts(now_str=now_str)
        assert now_str == timer.ts2str(now_ts=now_ts)
        week = timer.iso_week()
        assert "W" in week
        assert week.startswith("W") is False
        assert week.endswith("W") is False


if __name__ == "__main__":
    TestTimer()

"""
Functions for debugging.
"""
from datetime import datetime
from functools import wraps
from pathlib import Path

# Set this flag to turn on debugging.
DEBUG = True

# The root directory of the module, and a folder for logs.
MODULE_DIR = Path(__file__).parent.resolve()
LOG_DIR = MODULE_DIR / "logs"

# Format for datetime in log file name.
LOG_DATE_FMT = "%Y%m%d_%H%M%S"

_current_log = None


def if_debugging(func):
    """
    Decorator which only runs the function if DEBUG is true.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        """
        The wrapped function.
        """
        if DEBUG:
            return func(*args, **kwargs)
    return wrapper


@if_debugging
def create_dbglog():
    """Create a file to be the debug log for this run."""
    LOG_DIR.mkdir(exist_ok=True)
    log_file = LOG_DIR / f"dbg_{datetime.now().strftime(LOG_DATE_FMT)}"
    _current_log = open(log_file, "w")

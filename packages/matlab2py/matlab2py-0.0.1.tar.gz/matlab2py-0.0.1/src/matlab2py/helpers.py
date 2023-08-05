"""
Helper classes to mirror Matlab content
"""
from collections import namedtuple

# Named tuple so indexing bits of it is easier.
SwitchState = namedtuple("SwitchState", ["bool", "str", "int"])


class OnOffSwitchState(object):
    """Mirrors matlab.lang.OnOffSwitchState."""

    on = SwitchState(bool=True, str="on", int=1)
    off = SwitchState(bool=False, str="off", int=0)

    def __init__(self, value):
        """Can be set to on, off, true, false, or 1 or 0."""
        sanitised = value.lower() if isinstance(value, str) else value
        if sanitised not in (self.on + self.off):
            raise ValueError(f"'{value}' is not valid for a SwitchState.")
        self.called_val = value
        self.value = sanitised in self.on

    def __bool__(self):
        """True if in on, false if in off."""
        if self.value:
            return self.on.bool
        else:
            return self.off.bool

    def __str__(self):
        """For putting the on/off state in a string, use the string version."""
        if self.value:
            return self.on.str
        else:
            return self.off.str

"""
Entry point for figures.
"""
import subprocess
import sys
from functools import partial, update_wrapper
from platform import system

from screeninfo import get_monitors

from constants import (
    AX_DEFAULT_POS,
    DPI_ON_DARWIN,
    DPI_ON_WINDOWS,
    FIG_DEFAULT_COLOR,
)
from helpers import OnOffSwitchState
from singleton import Singleton


def var_to_str(arr):
    """Numpy array to a string which can be executed."""
    return (
        f"np.ndarray(shape={arr.shape}, dtype=np.{arr.dtype.name}, "
        f"buffer={arr.tobytes()})"
    )


def is_fig_number_valid(number):
    """Assert that a figure number is a valid positive integer."""
    if isinstance(number, int) and number > 0:
        return True
    else:
        return False


def add_name_value_pair(name, cls, default):
    """Adds a name-value pair, including defining suitable setter and getter."""

    pvt_name = f"_{name}"

    def getter(self):
        return getattr(self, pvt_name)

    def setter(self, value):
        setattr(self, pvt_name, cls(value))

    setattr(FigureHandle, name, property(getter, setter))
    setattr(FigureHandle, pvt_name, default)


def make_property(prop_cls, prop_default, autoset=True):
    """Turns the wrapped function into the setter of a property """
    def wrapper(fset):
        fset.prop = True
        fset.prop_cls = prop_cls
        fset.prop_default = prop_default
        fset.prop_autoset = autoset
        return fset
    return wrapper


def construct_properties(cls):
    """Turn the properties into properties."""

    def getter(pvt_name, self):
        """The getter for this property."""
        return getattr(self, pvt_name)

    def setter(pvt_name, prop_class, method, self, value):
        """Set the value, forcing the type, then run the rest."""
        setattr(self, pvt_name, prop_class(value))
        method(self, value)

    clsdict = {x: y for x, y in cls.__dict__.items() if hasattr(y, "prop")}

    for name, method in clsdict.items():
        print(
            f"making property from: {name} ({method.prop}, "
            f"{method.prop_cls.__name__}, {method.prop_default}, "
            f"{method.prop_autoset})"
        )
        pvt_name = f"_{name}"

        get_fn = update_wrapper(partial(getter, pvt_name), method)
        set_fn = (
            partial(setter, pvt_name, method.prop_cls, method)
            if method.prop_autoset else partial(method)
        )

        setattr(cls, name, property(get_fn, set_fn))
        setattr(cls, pvt_name, method.prop_cls(method.prop_default))

    return cls


class PlotHandle(object):
    """Handle to a plot."""

    def __init__(self, ax, x, y):
        self.parent = ax
        self.parent.parent._cmd(
            f"{self.parent.ref}.plot({var_to_str(x)},{var_to_str(y)})"
        )


class AxesHandle(object):
    """Handle to an axis."""

    def __init__(self, fig, number, position):
        self.parent = fig
        self.idx = number
        self.ref = f"fig.axes[{number}]"
        self._children = []
        self.parent._cmd(f"{self.parent.ref}.add_axes({position})")

    def _plot(self, x, y):
        """Plot a line into this axes."""
        return PlotHandle(self, x, y)


@construct_properties
class FigureHandle(object):
    """Handles sending stuff to the subprocess."""

    def __init__(self, number, parent):
        """Setup the handle which includes starting the subprocess."""
        self.is_current = False
        self._Number = number
        self._children = []
        self._current_child = None
        self._parent = parent
        self.ref = "fig"

        # Do as much as we can before this.
        self.process = subprocess.Popen(
            [f"{sys.executable}", "figure_process.py", str(number)],
            startupinfo=subprocess.STARTUPINFO(
                dwFlags=subprocess.DETACHED_PROCESS,
            ),
            stdin=subprocess.PIPE,
            stdout=open("out.log", "w"),
            universal_newlines=True,
            bufsize=1,
        )

    # Public methods which are python-specific

    @property
    def current_child(self):
        """The index of the currently active child."""
        print(f"children: {self._children}")
        print(f"current_child: {self._current_child}")
        return self._children[self._current_child]

    @current_child.setter
    def current_child(self, value):
        """Current child setter (must set by index)."""
        assert(isinstance(value, int))
        assert(value > 0)
        self._current_child = value - 1

    def add_axes(self, position=AX_DEFAULT_POS):
        """Add an axes as a child."""
        new_ax_num = len(self._children)
        print(f"Assigning new ax: {new_ax_num}")
        ax = AxesHandle(self, new_ax_num, position)
        self._children.append(ax)
        self._current_child = new_ax_num
        return ax

    # Public methods which mirror MATLAB properties.

    @make_property(int, 0, autoset=False)
    def Number(self, number):
        """Can only set number to a positive integer not currently in use."""
        # TODO update figure title here.
        if number != self._Number:
            # If we already have that number, do nothing.
            self._parent.change_figure_number(self._Number, number)
            self._Number = number
            self._update_window_title()

    @make_property(OnOffSwitchState, "on")
    def NumberTitle(self, onoffswitch):
        """Turn on or off the 'Figure #' in the title of the figure."""
        self._update_window_title()

    @make_property(str, "")
    def Name(self, name):
        """Give the figure an arbitrary name."""
        self._update_window_title()

    @make_property(list, [0, 0, 100, 100])
    def Position(self, pos):
        """Sets the position of the figure."""
        pass

    @make_property(list, list(FIG_DEFAULT_COLOR))
    def Color(self, col):
        """
        Set the background color of the figure.
        """
        self._cmd(f"fig.patch.set_facecolor({tuple(self._Color)})")

    # Private Methods

    def _cmd(self, cmds, add_update=True):
        """
        Send commands to the child process (which contains the figure). At the
        point that the commands are executed, the only accessible variable is
        `fig` which is the matplotlib Figure() in question. Hence, all access to
        e.g. the axes must be by using figure properties.
        """
        # Force a sequence.
        if not isinstance(cmds, (list, tuple)):
            cmds = [cmds]

        # Write the commands, appending a newline.
        for cmd in cmds:
            self.process.stdin.write(f"{cmd}\n")

        # If we need to force an update (we usually do to make the figure
        # respond), we need to draw and flush the canvas.
        if add_update:
            self.process.stdin.write("fig.canvas.draw()\n")
            self.process.stdin.write("fig.canvas.flush_events()\n")

    def _update_window_title(self):
        """Update the window title."""
        number_prefix = f"Figure {self.Number}" if self.NumberTitle else ""
        connector = ": " if self.NumberTitle and self.Name else ""
        title = number_prefix + connector + self.Name
        self._cmd(f"fig.canvas.manager.set_window_title('{title}')")

    def _update_window_position(self):
        """Update the window position."""


@construct_properties
class GraphicsRootHandle(Singleton):
    """Graphics root properties, always the 0th figure."""

    def __init__(self):
        """__init__ must do nothing for a singleton."""
        pass

    def init(self):
        """Initialise."""
        # Populate the monitors data.
        self._monitors = []
        self._update_monitors()

        self._system = system()

    def __repr__(self):
        return f"GraphicsRootHandle({self.__dict__})"

    @property
    def ScreenSize(self):
        """The pixel size of the screen."""
        for mon in self._monitors:
            if mon.is_primary:
                return [mon.x + 1, mon.y + 1, mon.width, mon.height]

    @property
    def ScreenPixelsPerInch(self):
        """
        Readonly since R2015b.
        :return: scalar
        """
        if self._system == "Windows":
            return DPI_ON_WINDOWS
        elif self._system == "Darwin":
            return DPI_ON_DARWIN
        else:
            raise NotImplementedError("DPI on Linux not working yet.")

    # Private Methods

    def _update_monitors(self):
        """Update the monitors list."""
        self._monitors = get_monitors()


class FigureHandlesArray(Singleton):
    """The array of figure handles. 0 is the graphics root."""

    def __init__(self):
        """
        Required for anything inheriting from Singleton that __init__ does
        nothing.
        """
        pass

    def init(self):
        """
        Create a FigureHandlesArray.
        """
        self._current_fig_num = 0

        # Store figures as a dict mapping figure number to the handle. Figure
        # zero is the graphics root.
        self._figures = {0: GraphicsRootHandle()}

    def __getitem__(self, number):
        """Gets figure number from the array."""
        print(f"getitem: {number}")
        return self._figures[number]

    @property
    def current_fig(self):
        """Get FigureHandle to the current figure."""
        return self._figures[self._current_fig_num]

    @current_fig.setter
    def current_fig(self, number):
        """Set current_fig to an integer to make the fig number current."""
        # TODO make this raise a proper error.
        assert(self._is_existing_number_valid(number))

        self._figures[self._current_fig_num].is_current = False
        self._current_fig_num = number
        self._figures[self._current_fig_num].is_current = True

    def _is_existing_number_valid(self, number):
        """Test if number is a valid existing figure."""
        if is_fig_number_valid(number) and number in self._figures.keys():
            return True
        else:
            return False

    def _is_new_number_valid(self, number):
        """Test if number is valid for a new figure."""
        if is_fig_number_valid(number) and number not in self._figures.keys():
            return True
        else:
            return False

    def _get_next_fig_num(self):
        """Find the lowest number which is not used as a figure number."""
        # Because use cases for many many figures are rare, just count up from
        # one and return the first which passes.
        next_num = 0
        while True:
            if self._is_new_number_valid(next_num):
                return next_num
            else:
                next_num += 1

    def make_new_figure(self, number=None, properties=None):
        """Start a new figure and return its handle."""
        new_fig_num = (
            number if self._is_new_number_valid(number)
            else self._get_next_fig_num()
        )
        fig = FigureHandle(new_fig_num, self)
        self._figures[new_fig_num] = fig
        self._current_fig_num = new_fig_num
        if properties is None:
            properties = {}
        for name, value in properties.items():
            setattr(fig, name, value)
        return fig

    def change_figure_number(self, current_num, new_num):
        """Change the figure with current_num to new_num."""
        if self._is_new_number_valid(new_num):
            self._figures[new_num] = self._figures.pop(current_num)
        else:
            raise ValueError(f"Figure {new_num} is already in use!")

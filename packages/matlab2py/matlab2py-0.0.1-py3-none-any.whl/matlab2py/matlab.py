"""
Functions with MATLAB-compatible signatures.
"""
from handles import FigureHandlesArray, FigureHandle

# All of the figure handles.
HANDLES = FigureHandlesArray()
groot = HANDLES[0]


def axes(fig):
    """Add an axes to fig."""
    fig.add_axes()


def figure(*args):
    """
    Create a new figure or make an existing one current.

    Mirrors: matlab.ui.figure

    Signatures:
    figure()
    figure(handle)
    figure(number)
    figure(name, value, ...)
    f = figure(___)
    """
    print(f"figure args: {args}")
    if not args:
        print("Empty args")
        return HANDLES.make_new_figure()

    elif len(args) == 1:
        print("1 arg")
        if isinstance(args[0], int):
            # Find figure with number int or make a new one.
            try:
                print("trying")
                HANDLES.current_fig = args[0]
                return HANDLES[args[0]]
            except (KeyError, AssertionError):
                print("excepting")
                return HANDLES.make_new_figure(number=args[0])

        elif isinstance(args[0], FigureHandle):
            print("handle passed")
            # Make that figure the current figure and bring to front.
            HANDLES.current_fig = args[0].Number
            return args[0]

    elif len(args) % 2 == 0:
        print("name value")
        # We've got name-value pairs.
        assert(all(isinstance(x, str) for x in args[::2]))
        return HANDLES.make_new_figure(
            properties={
                name: value for name, value in zip(args[0::2], args[1::2])
            },
        )

    else:
        # Error?
        ValueError("Invalid number of arguments.")


def gca():
    """Return the current axes."""
    return gcf().current_child


def gcf():
    """Return the current figure."""
    print(f"current_fig number: {HANDLES.current_fig._Number}")
    print(f"figures: {HANDLES._figures}")
    return HANDLES.current_fig


def plot(ax, x, y):
    """Plot """
    return ax._plot(x, y)

"""
Plotting machinery
"""
import queue
import sys
import threading
import time

import matplotlib.pyplot as plt
import numpy as np  # Needed for dynamic code.

from argparse import ArgumentParser


def rate_limited_true():
    """Returns true after a given delay."""
    time.sleep(0.05)
    return True


def parser():
    """The argparser."""
    parser = ArgumentParser()
    parser.add_argument("num")
    return parser


def add_stdin_to_queue(input_queue):
    """Listen to stdin for new data."""
    while rate_limited_true():
        input_queue.put(sys.stdin.readline())
        print(input_queue)


def update_plot(input_queue, fig):
    """Wait for things in the queue."""
    while rate_limited_true():
        if not input_queue.empty():
            command = input_queue.get()
            if command:
                exec(command)


def make_thread(fn, args):
    """Makes a new thread for this process."""
    thread = threading.Thread(target=fn, args=args)
    thread.daemon = True
    thread.start()
    return thread


def main(args):
    fig = plt.figure(f"Figure {args.num}")

    input_queue = queue.Queue()

    input_thread = make_thread(fn=add_stdin_to_queue, args=(input_queue,))
    plot_thread = make_thread(fn=update_plot, args=(input_queue, fig))

    plt.show()


if __name__ == "__main__":
    main(parser().parse_args())

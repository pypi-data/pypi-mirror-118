"""
Development entry point.
"""
import numpy as np

from matlab import figure, axes, gca, gcf, groot, plot

if __name__ == "__main__":

    g = groot
    print(g)
    print("between")
    print(g.ScreenSize)

    print("\n*** figure() ***")
    figure(5)
    print("\n*** axes(gcf()) ***")
    axes(gcf())

    print("\n*** figure('NumberTitle','off','Name','TestFig') ***")
    f2 = figure('Name', 'TestFig', 'NumberTitle', 'off')
    print(f2.Name)
    print(f2.NumberTitle)

    print("\n*** figure('Name','Test2') ***")
    figure('Name', 'Test2')

    print("\n*** figure(1) ***")
    f = figure(5)

    print("\n*** ax = gca() ***")
    ax = gca()
    print(f"ax: {ax}")

    x = np.linspace(0, 10, num=100)
    y = np.sin(x)
    plot(ax, x, y)
    print(f.Name)

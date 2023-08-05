"""
Constants baked into MATLAB.
"""

# DPI is fixed on Windows and Mac (Darwin), since R2015b, and is also read-only.
# https://www.mathworks.com/help/matlab/ref/matlab.ui.root-properties.html
DPI_ON_WINDOWS = 96.0
DPI_ON_DARWIN = 72.0

# Axes default location within a figure (in figure coordinates).
# https://www.mathworks.com/help/matlab/ref/matlab.graphics.axis.axes-properties.html#d123e62844
AX_DEFAULT_POS = (0.1300, 0.1100, 0.7750, 0.8150)

# Default background color for figures, given as a normalised 3-vector.
# Can't find a reference, so I tested it on R2020b.
FIG_DEFAULT_COLOR = (0.94, 0.94, 0.94)

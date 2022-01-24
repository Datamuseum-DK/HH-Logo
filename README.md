# HH-Logo

Python code to create HH Logo

Inspired by Figure 10 in:

    "Den Elektroniske Cifferregnemaskine

    ved Regnecentralen

    Dansk Institut for Matematikmaskiner"

By B. Scharøe Petersen

Available at: https://datamuseum.dk/bits/30002303

The basic python class expects at least `line_to` and `draw_to`
methods, but will also use `set_line_width` and `curve_to` if
available.

If now drawer class is available, a list of drawing primitives
to perform is returned instead.

The logo fits inside [0,0]...[1000,1000], Y-axis is down.

/phk

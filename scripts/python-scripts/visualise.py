import numpy as np
import plotly.graph_objs as go


def set_interval_value(x, a, b):
    # function that associate to a float x, a value encoding its position with respect to the interval [a, b]
    #  the associated values are 0, 1, 2 assigned as follows:
    if x <= a:
        return 0
    elif a < x <= b:
        return 1
    else:
        return 2


def data2color(x, y, a, b, c, d, biv_colors):
    # This function works only with a list of 9 bivariate colors, because of the definition of set_interval_value()
    # x, y: lists or 1d arrays, containing values of the two variables
    # each x[k], y[k] is mapped to an int  value xv, respectively yv, representing its category,
    # from which we get their corresponding color  in the list of bivariate colors
    # number of colours
    n_colors = len(biv_colors)

    if len(x) != len(y):
        raise ValueError("the list of x and y-coordinates must have the same length")
    if n_colors != 9:
        raise ValueError(
            "the list of bivariate colors must have the length eaqual to 9"
        )

    xcol = [set_interval_value(v, a, b) for v in x]
    ycol = [set_interval_value(v, c, d) for v in y]

    n = 3

    # index of the corresponding color in the list of bivariate colors
    idxcol = [int(xc + n * yc) for xc, yc in zip(xcol, ycol)]
    colors = np.array(biv_colors)[idxcol]

    return list(colors)


def colorsquare(text_x, text_y, colorscale, n=3, xaxis="x2", yaxis="y2"):
    # text_x : list of n strings, representing intervals of values for the first variable or its n percentiles
    # text_y : list of n strings, representing intervals of values for the second variable or its n percentiles
    # colorscale: Plotly bivariate colorscale
    # returns the colorsquare as alegend for the bivariate choropleth, heatmap and more

    z = [[j + n * i for j in range(n)] for i in range(n)]
    n = len(text_x)
    if len(text_x) != n or len(text_y) != n or len(colorscale) != 2 * n ** 2:
        raise ValueError(
            "Your lists of strings  must have the length {n} and the colorscale, {n**2}"
        )

    text = [
        [text_x[j] + "<br>" + text_y[i] for j in range(len(text_x))]
        for i in range(len(text_y))
    ]
    return go.Heatmap(
        x=list(range(n)),
        y=list(range(n)),
        z=z,
        xaxis=xaxis,
        yaxis=yaxis,
        text=text,
        hoverinfo="text",
        colorscale=colorscale,
        showscale=False,
    )


def colors_to_colorscale(biv_colors):
    # biv_colors: list of n**2 color codes in hexa or RGB255
    # returns a discrete colorscale  defined by biv_colors
    n = len(biv_colors)
    biv_colorscale = []
    for k, col in enumerate(biv_colors):
        biv_colorscale.extend([[round(k / n, 2), col], [round((k + 1) / n, 2), col]])
    return biv_colorscale

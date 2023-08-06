# -*- encoding: utf-8 -*-


from ._constants import _PRECISION
from ._helpers import _format_value, _format_point, _format_points, _diff_points, _diff


def line(
    points: list[tuple[float, float]],
    precision: int = _PRECISION,
    absolute: bool = False,
) -> str:
    if absolute:
        return "M" + _format_points(points, precision)
    else:
        points_diff = [points[0], *_diff_points(points)]
        return "m" + _format_points(points_diff, precision)


def area(
    points: list[tuple[float, float]],
    fill_to: float = 0,
    precision: int = _PRECISION,
    absolute: bool = False,
) -> str:
    points = [(points[0][0], fill_to), *points, (points[-1][0], fill_to)]
    return line(points, precision=precision, absolute=absolute) + " z"


def ribbon(
    low_high_points: list[tuple[float, float, float]],
    precision: int = _PRECISION,
    absolute: bool = False,
) -> str:
    points = [
        *((point[0], point[1]) for point in low_high_points),
        *((point[0], point[2]) for point in low_high_points[::-1]),
    ]
    return line(points, precision=precision, absolute=absolute) + " z"


def rug(
    x: list[float],
    y: float = 0,
    line_height: float = 1,
    precision: int = _PRECISION,
    absolute: bool = False,
) -> str:
    if absolute:
        return " ".join(
            f"M{_format_point(x_i, y - (line_height / 2), precision)}"
            + f"V{_format_value(y + (line_height / 2), precision)}"
            for x_i in x
        )
    else:
        x_diff = [x[0], *_diff(x)]
        return f"m{_format_point(0, y + (line_height / 2), precision)} " + " ".join(
            f"m{_format_point(x_i, -line_height, precision)}"
            + f"v{_format_value(line_height, precision)}"
            for x_i in x_diff
        )

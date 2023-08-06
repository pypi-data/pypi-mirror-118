# -*- encoding: utf-8 -*-


def _format_value(value, precision):
    return f"{value:0.{precision}g}"


def _format_point(x, y, precision):
    return f"{x:0.{precision}g},{y:0.{precision}g}"


def _format_points(points, precision):
    return " ".join([_format_point(*point, precision) for point in points])


def _diff_points(points):
    return [
        ((p2[0] - p1[0]), (p2[1] - p1[1])) for (p1, p2) in zip(points[:-1], points[1:])
    ]


def _diff(x):
    return [x2 - x1 for (x1, x2) in zip(x[:-1], x[1:])]

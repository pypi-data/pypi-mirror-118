# -*- encoding: utf-8 -*-


from ._constants import _PRECISION
from ._helpers import _format_point
from .basic import rug as _rug


def raster(
    raster_data: list[list[float]],
    line_height: float = 1,
    inter_trial_distance: float = 1,
    precision: int = _PRECISION,
    absolute: bool = False,
) -> str:
    if absolute:
        return "  ".join(
            [
                _rug(
                    raster_trial,
                    y=(trial_n * inter_trial_distance),
                    line_height=line_height,
                    precision=precision,
                    absolute=absolute,
                )
                for (trial_n, raster_trial) in enumerate(raster_data)
            ]
        )
    else:
        path_d = ""
        for trial_n, raster_trial in enumerate(raster_data):
            path_d += _rug(
                raster_trial,
                y=(0 if trial_n == 0 else inter_trial_distance),
                line_height=line_height,
                precision=precision,
                absolute=absolute,
            )
            path_d += (
                f"  m{_format_point(-raster_trial[-1], -line_height / 2, precision)}  "
            )
        return path_d

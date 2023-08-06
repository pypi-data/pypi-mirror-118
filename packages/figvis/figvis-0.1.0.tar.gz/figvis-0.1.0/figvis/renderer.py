# -*- encoding: utf-8 -*-

from pathlib import Path

from jinja2 import Environment as _Environment
from jinja2 import FileSystemLoader as _FileSystemLoader
import numpy as _np

from figvis import data, figment, transform


FIGVIS_TEMPLATES_PATH = [Path(__file__).parent.joinpath("templates").resolve()]


def render(
    template_paths: list[Path],
    source: Path,
    exclude_figvis_templates: bool = False,
    **options
):
    template_paths = [source.parent] + template_paths
    if not exclude_figvis_templates:
        template_paths += FIGVIS_TEMPLATES_PATH
    template_paths = [str(template_path) for template_path in template_paths]
    jinja_environment = _Environment(
        loader=_FileSystemLoader(template_paths, followlinks=True))
    template = jinja_environment.get_template(str(source.name))
    return template.render(
        data=data, transform=transform, figment=figment,
        inf=_np.inf, np=_np, **options
    )

# -*- encoding: utf-8 -*-

from pathlib import Path

from jinja2 import Environment, FileSystemLoader


FIGVIS_TEMPLATES_PATH = [Path(__file__).parent.joinpath("templates")]


def render(
    template_paths: list[Path],
    source: Path,
    exclude_figvis_templates: bool = False
):
    if exclude_figvis_templates:
        jinja_environment = Environment(
            loader=FileSystemLoader(template_paths, followlinks=True))
    else:
        jinja_environment = Environment(
            loader=FileSystemLoader(
                FIGVIS_TEMPLATES_PATH + template_paths, followlinks=True))
    template = jinja_environment.get_template(source)
    return template.render()

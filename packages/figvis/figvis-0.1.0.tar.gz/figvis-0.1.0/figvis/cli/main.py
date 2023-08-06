#! /usr/bin/env python3
# -*- encoding: utf-8 -*-


from pathlib import Path
from typing import Optional, List

import typer

from figvis.svg_to_pdf import svg_to_pdf as _svg_to_pdf
from figvis.renderer import render as _render

app = typer.Typer(help="Figment Visualization")


@app.command(help="Convert SVG to PDF using Inkscape or Firefox")
def svg_to_pdf(
    svg_file_path: Path = typer.Argument(..., help="Input SVG file"),
    pdf_file_path: Path = typer.Argument(..., help="Output PDF file"),
    firefox: Optional[bool] = typer.Option(
        False, help="Use Firefox for conversion"),
):
    _svg_to_pdf(svg_file_path.resolve(),
                pdf_file_path.resolve(), firefox=firefox)


@app.command(help="Render a jinja2 template")
def render(
        input: Path = typer.Argument(..., help="Template source file"),
        output: Path = typer.Argument(..., help="Rendered input"),
        templates: Optional[List[Path]] = typer.Option(
            [], help="Templates folder"),
        exclude_figvis_templates: Optional[bool] = typer.Option(
            False, help="Exclude templates bundled with FigVis framework"),
):
    with open(output, 'w') as output_handle:
        output_handle.write(_render([template.resolve() for template in templates],
                                    input.resolve(),
                                    exclude_figvis_templates=exclude_figvis_templates))


if __name__ == "__main__":
    app()

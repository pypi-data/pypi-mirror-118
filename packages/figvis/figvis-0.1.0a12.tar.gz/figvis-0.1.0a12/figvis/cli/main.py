#! /usr/bin/env python3
# -*- encoding: utf-8 -*-


from pathlib import Path

import typer

from figvis.svg_to_pdf import svg_to_pdf as svg_to_pdf_

app = typer.Typer(help="Figment Visualization")


@app.command()
def svg_to_pdf(
    svg_file_path: Path = typer.Argument(..., help="Input SVG file"),
    pdf_file_path: Path = typer.Argument(..., help="Output PDF file"),
):
    svg_to_pdf_(svg_file_path.resolve(), pdf_file_path.resolve())


if __name__ == "__main__":
    app()

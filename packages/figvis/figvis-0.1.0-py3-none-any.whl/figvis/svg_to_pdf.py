# -*- encoding: utf-8 -*-

from base64 import b64decode
from pathlib import Path
import subprocess

from lxml import etree
from selenium.webdriver import Firefox, FirefoxOptions
from selenium.webdriver.common.print_page_options import PrintOptions


def svg_to_pdf(
    svg_file_path: Path,
    pdf_file_path: Path,
    firefox: bool = False,
):
    if firefox:
        svg_dimensions = dimensions(svg_file_path)
        firefox_options = FirefoxOptions()
        firefox_options.headless = True
        with Firefox(options=firefox_options) as firefox:
            print_options = PrintOptions()
            print_options.margin_top = 0
            print_options.margin_bottom = 0
            print_options.margin_left = 0
            print_options.margin_right = 0
            print_options.scale = 1
            print_options.shrink_to_fit = False
            print_options.page_ranges = ["1"]
            print_options.page_width = svg_dimensions["width"]
            print_options.page_height = svg_dimensions["height"]
            firefox.get(svg_file_path.as_uri())
            pdf_data = b64decode(firefox.print_page(
                print_options=print_options))
        with open(pdf_file_path, "wb") as output_file:
            output_file.write(pdf_data)
    else:
        subprocess.run(['inkscape', '-o', pdf_file_path, svg_file_path])


def dimensions(svg_file_path: Path):
    svg = etree.parse(str(svg_file_path)).getroot()
    return {
        "width": to_cm(svg.get("width")),
        "height": to_cm(svg.get("height"))
    }


def to_cm(quantity: str) -> float:
    unit = quantity[-2:].lower()
    value = float(quantity[:-2])
    if unit == "cm":
        value_cm = value
    elif unit == "mm":
        value_cm = value / 10
    elif unit == "in":
        value_cm = value * 2.54
    elif unit == "pt":
        value_cm = (value / 72) * 2.54
    elif unit == "pc":
        value_cm = ((value * 12) / 72) * 2.54
    return value_cm

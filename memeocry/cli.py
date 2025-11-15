import os

import click

from .ocr import search, update

images_path = os.path.abspath("images")


@click.group()
@click.version_option()
def cli():
    "DESCRIPTION"


@cli.command(name="update")
@click.argument("folder")
def update_command(folder):
    number_updated = update(folder, ["de", "en"])
    click.echo(
        f"OCRed {number_updated} images in {folder} and stored texts in memeocry.json."
    )


@cli.command(name="search")
@click.argument("text")
def search_command(text):
    "Command description goes here"
    results = search(text)
    if results:
        click.echo(create_search_results(results))
    else:
        click.echo("No search result.")


def create_search_results(search_results):
    return "\n".join(
        [
            create_search_result(search_result, index)
            for index, search_result in enumerate(search_results)
        ]
    )


def create_search_result(search_result, index):
    rel_path = search_result["path"]
    abs_path = os.path.abspath(rel_path)
    link = create_file_link(abs_path, rel_path)
    excerpt = search_result["text"][:30]
    return f"{index + 1}. {link} {excerpt}"


def create_file_link(filepath, text=None):
    """Create a clickable terminal link to a file"""
    if text is None:
        text = filepath

    # OSC 8 hyperlink format: \033]8;;http://example.com\033\\This is a link\033]8;;\033\\
    link = f"\033]8;;file://{filepath}\033\\{text}\033]8;;\033\\"
    return click.style(link, fg="blue", underline=True)

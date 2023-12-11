import os

import typer
from rich.console import Console

from fast_arxiver.utils import markdown_template, get_article, get_ollama_response

app = typer.Typer(help="Archive page for arxiv.org")
console = Console()


@app.command()
def main(
    arxiv_url: str,
    path_to_archive_folder: str = "~/Documents/Main Obsidian/Research/Papers/",
    dont_suggest_keywords: bool = False,
):
    result = get_article(arxiv_url)
    console.print(f'Found "{result.title}" article.')
    file_text = markdown_template.format(
        date=result.published.strftime("%Y-%m"),
        authors=", ".join(f"[[{a.name}]]" for a in result.authors),
        entry_id=result.entry_id,
        summary=result.summary.replace("\n", " "),
    )
    file_name = result.title.split(":")[0].strip() + ".md"
    file_path = os.path.expanduser(os.path.join(path_to_archive_folder, file_name))
    if os.path.exists(file_path):
        console.print(f"{file_name} is already archived. Check obsidian files")
    else:
        with open(file_path, "w") as result_file:
            result_file.write(file_text)
        console.print(f"All done. {file_name} have been archived!")

    if not dont_suggest_keywords:
        suggest_keywords_for_article(arxiv_url)


@app.command()
def suggest_keywords_for_article(
    arxiv_url: str,
    path_to_key_items_folder: str = "~/Documents/Main Obsidian/KeyItems/",
):
    result = get_article(arxiv_url)
    key_items = list()
    for file in os.listdir(os.path.expanduser(path_to_key_items_folder)):
        if file.endswith(".md"):
            key_items.append(file[:-3])
    result = get_ollama_response(result.title, result.summary, key_items)
    console.print(f"Ollama suggestions for keywords: {result}")


if __name__ == "__main__":
    app()

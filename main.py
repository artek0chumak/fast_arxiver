import arxiv
import typer
import os
from rich.console import Console

app = typer.Typer(help="Archive page for arxiv.org")
console = Console()

markdown_template = """---
publication_date: {date}
status: Waiting
---

authors:: {authors}
[arxiv]({entry_id})
key_items::

## Abstract
{summary}
"""


def url_to_id(url: str) -> str:
    """
    Parse the given URL of the form `https://arxiv.org/abs/1907.13625` to the id `1907.13625`.

    Args:
        url: Input arxiv URL.

    Returns:
        str: ArXiv article ID.
    """
    # Strip filetype
    if url.endswith(".pdf"):
        url = url[:-4]

    return url.split("/")[-1]


@app.command()
def main(arxiv_url: str, path_to_archive_folder: str = "~/Documents/Main Obsidian/Research/Papers/"):
    article_id = url_to_id(arxiv_url)
    arxiv_result = arxiv.Search(id_list=[article_id])
    results = list(arxiv_result.results())
    result = results[0]
    console.print(f"Found {len(results)} articles. Will use first one to archive.")
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


if __name__ == "__main__":
    app()

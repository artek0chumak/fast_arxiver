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

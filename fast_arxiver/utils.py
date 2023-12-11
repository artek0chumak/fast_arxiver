import arxiv
import httpx
import logging
import random

from typing import Optional


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


keywords_prompt = """There are all of the keywords:
{keywords}

Read article summary and suggest top 10 keywords for it:
{title}
{summary}
Keywords:"""


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


def get_article(arxiv_url: str) -> arxiv.Result:
    article_id = url_to_id(arxiv_url)
    arxiv_result = arxiv.Search(id_list=[article_id])
    results = list(arxiv_result.results())
    return results[0]


def get_ollama_response(
    article_title: str,
    article_summary: str,
    keywords: list[str],
    ollama_url: str = "http://localhost:11434",
    model_name: Optional[str] = None,
    max_model_size: int = 1e10,
) -> str:
    prompt = keywords_prompt.format(
        title=article_title,
        summary=article_summary,
        keywords="\n".join(keywords),
    )
    if model_name is None:
        local_models = httpx.get(ollama_url + "/api/tags").json()["models"]
        if len(local_models) == 0:
            raise ValueError(
                "Cannot find any local model. Please, pull one using terminal."
            )
        model_size = max_model_size
        for model_info in local_models:
            if model_size > model_info.get("size", max_model_size):
                model_size = model_info.get("size")
                model_name = model_info["name"]

    response = httpx.post(
        ollama_url + "/api/generate",
        json={"model": model_name, "prompt": prompt, "stream": False},
        timeout=120,
    )
    return response.json()["response"]

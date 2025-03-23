import argparse
import json
from pathlib import Path

import yaml
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document
from langchain_core.language_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from ai_lab_radar.news_client import get_articles
from ai_lab_radar.to_html import render_articles

default_prompt = """Write a concise summary (output format: HTML with open and closing <html></html> tags) of the 
following articles that includes AI related developments:\\n\\n{context}"""


def create_document(article_dict: dict) -> Document:
    """
    Convert News API article dict to a LangChain document.

    :param article_dict: dict containing article data. Required keys: title, description, content
    :return: LangChain document
    """
    return Document(
        page_content=f"{article_dict['title']}\n\n{article_dict['description']}\n\n{article_dict['content']}"
    )


def summarize_stuff(llm: BaseChatModel, prompt: str, docs: list[Document]) -> str:
    """
    Uses create_stuff_documents_chain to generate a summary of all articles.

    :param llm: language model
    :param prompt: prompt template
    :param docs: list of documents
    :return: summary string
    """

    # Define prompt
    prompt = ChatPromptTemplate.from_messages(
        [("system", prompt)]
    )

    # Instantiate chain
    chain = create_stuff_documents_chain(llm, prompt)

    # Invoke chain
    result = chain.invoke({"context": docs})
    return result


def store_articles(articles: list[dict]) -> None:
    """
    Stores a list of news articles in JSON format to file articles.json in the current working directory.

    :param articles: a list of articles. Each article requires keys: title, description, content.
    """
    with open(Path.cwd() / "articles.json", "w") as fp:
        json.dump(articles, fp, indent=2)


def main() -> None:
    """
    Main function of AI Lab Radar, which creates an HTML document containing information on AI related developments.

    :return: None
    """

    # Parse arguments:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--cached", help="Use cached articles",  action="store_true")
    parser.add_argument(
        "-n", "--no-llm", help="Skip LLM call and concatenate all articles", action="store_true"
    )
    args = parser.parse_args()

    # Load config file:
    config_path = Path.cwd() / "config.yaml"
    if config_path.exists():
        print("Loading config.yaml...")
        with open(Path.cwd() / "config.yaml", "r") as fp:
            config = yaml.load(fp, Loader=yaml.SafeLoader)
    else:
        print("No config.yaml found, using default values")
        config = {}

    # Obtain articles:
    if args.cached:
        print("Use cached articles.")
        with open(Path.cwd() / "articles.json") as fp:
            articles = json.load(fp)
    else:
        print("Retrieving new articles...")
        articles = get_articles()
        store_articles(articles)

    if args.no_llm:
        print("Skip LLM call")
        result = render_articles(articles)
    else:
        # Initiate model
        model_provider = config.get("model", {}).get("provider", "openai")
        model = config.get("model", {}).get("name", "gpt-4o-mini")
        print(f"Model: {model} from {model_provider}")
        llm = init_chat_model(model, model_provider=model_provider)

        # Summarize articles:
        docs = [
            create_document(article_dict)
            for article_dict in articles
        ]
        prompt = config.get("prompt", default_prompt)
        print(f"Prompt: {prompt}")
        result = summarize_stuff(llm, prompt, docs)

    with open(Path.cwd() / "airadar-report.html", "w") as fp:
        fp.write(result)


if __name__ == "__main__":
    main()

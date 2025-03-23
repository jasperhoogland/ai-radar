import dominate


def render_article(article: dict) -> str:
    """
    Renders html for a single article

    :param article: article dict
    :return: article html
    """
    return f""""<h3>{article['title']}</h3>\n<p>{article['description']}</p>\n<p>{article['content']}</p>\n"""


def render_articles(articles: list[dict]) -> str:
    """
    :param articles: list of article dicts
    :return: HTML page
    """
    doc = dominate.document(title='AI Lab Radar Report')

    with doc.head:
        dominate.tags.meta(charset="UTF-8")

    with doc:
        for article in articles:
            dominate.tags.h3(article["title"])
            dominate.tags.p(article["description"])
            dominate.tags.p(article["content"])

    return str(doc)
import os

import requests


def get_articles() -> list[dict]:
    """
    Make an API call to retrieve AI related articles.

    :return: a list of retrieved news articles
    """

    api_key = os.environ["NEWS_API_KEY"]

    x = requests.get(
        f'https://newsapi.org/v2/everything?q=AI&from=2025-02-23&sortBy=publishedAt&language=nl&apiKey={api_key}'
    )

    return x.json()["articles"]

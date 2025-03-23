# AI Lab Radar

AI Lab Radar finds AI related news articles and creates a report describing recent developments and emerging 
technologies in the field of AI.

## Setup

The AI Lab Radar requires 

* [News API](https://newsapi.org) to find AI related news articles,
* [OpenAI's GPT model](https://platform.openai.com) for summarization (by default), and
* [LangSmith](https://www.langchain.com/langsmith) for tracing LLM calls.

Sign up for these services if you aren't already registered (see links).
Once API keys for these services are obtained, set the following environment variables:
```
LANGSMITH_API_KEY=my_langsmith_api_key
LANGSMITH_TRACING=true
NEWS_API_KEY=my_news_api_key
OPENAI_API_KEY=my_open_api_key
```

To install the AI Lab Radar `git clone` this repo, `cd` into it, and `pip install` it:

```shell
git clone https://github.com/jasperhoogland/ai-radar
cd ai-radar
pip install .
```

## Usage

### Basic usage

The command
```shell
airadar
```
runs the AI radar and stores the result in `airadar-report.html` in the current working directory.

### Using cached articles
If the AI radar has been run before in the current working directory, then a file
called `articles.json` has been created.
By running
```shell
airadar --cached
```
the articles cached in this file are used, avoiding a new API call to News API.
An LLM call is still made in order to summarize the cached articles.

### Using a different model

By default, OpenAI's `gpt-4o-mini` model is used.
Different models can be used by specifying them in a `config.yaml` file in the current working directory.
For example, the following config uses OpenAI's `gpt-4o` model:
```yaml
model:
  provider: openai
  name: gpt-4o
```
Note that different model providers may require different environment variables to be set (yet to be tested).

### Using a different prompt

A default prompt is used if no prompt is provided.
This prompt is printed when the AI Lab Radar is invoked.
A different prompt can be used by providing it in the `config.yaml` file in the current working directory:
```yaml
prompt: "Compile a list of AI related developments and emerging technologies based on a list of news articles. 
Write the output as HTML with <html></html> tags. \\n\\n 
The articles are: {context}"
```

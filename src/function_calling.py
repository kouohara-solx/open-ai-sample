from openai import OpenAI  # (1)
import os
import sys
import requests
import streamlit as st
import logging
from bs4 import BeautifulSoup
from serpapi import GoogleSearch
from dotenv import load_dotenv
import json

load_dotenv()

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True)


def search_blog(param: dict) -> str:  # (2)
    """
    指定したキーワードでソルクシーズ公認ブログを検索して、URLのリストを得る。
    Args:
        param (dict): 検索キーワード
    Returns:
        str: URLのリスト
    """
    search_str = param["query_str"]
    search = GoogleSearch(
        {
            "q": f"site:solxyz-blog.info {search_str}",
            "api_key": os.getenv("SERPAPI_API_KEY"),
        }
    )  # (3)

    result = search.get_dict()
    address_list = [result["link"] for result in result["organic_results"]]
    return str(address_list)  # (4)


def get_blog_contents(param: dict) -> str:  # (2)
    """
    指定したURLのブログ記事の内容を取得する
    Args:
        param (dict): ブログ記事のURL
    Returns:
        str: ブログ記事の内容
    """
    blog_response = requests.get(param["url"])  # (3)
    soup = BeautifulSoup(blog_response.text, "html.parser")
    contents = soup.find("div", class_="content")
    texts = [c.get_text() for c in contents.find_all("p")]
    texts = "\n\n".join(texts)  # (4)

    return texts[:4000]  # (5)


tools = [
    {
        "type": "function",
        "function": {
            "name": "search_blog",
            "description": "指定したキーワードでソルクシーズ公認ブログを検索して、URLのリストを得る。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query_str": {
                        "type": "string",
                        "description": "検索キーワード",
                    },
                },
                "required": ["query_str"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_blog_contents",
            "description": "指定したURLについてその内容を取得して、パースした結果のテキストを得る。",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "内容を取得したいページのURL",
                    },
                },
                "required": ["url"],
            },
        },
    }
]

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

st.title("🐟Function Calling🐟")
query_str = st.text_input("検索ワードを入力してください。")

if query_str:
    question = f"""
    「```{query_str}```」について、まずソルクシーズ公認ブログを検索した結果のその上位3件を取得します。
    その後、それぞれのURLについてその内容を取得して、パースした結果のテキスト得ます。
    そしてそれらのパースした結果をまとめ、最終的な答えを１つ生成してください。
    """  # (1)

    MAX_REQUEST_COUNT = 10  # (2)

    message_history = []  # (3)

    for request_count in range(MAX_REQUEST_COUNT):  # (4)

        tool_choice = "auto"
        if request_count == MAX_REQUEST_COUNT - 1:
            tool_choice = "none"  # (5)
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "user", "content": question},
                *message_history,
            ],
            tools=tools,
            tool_choice=tool_choice,
        )  # (6)
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls
        if tool_calls:  # (7)
            available_functions = {
                "get_blog_contents": get_blog_contents,
                "search_blog": search_blog,
            }
            message_history.append(response_message)
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(function_args)  # (9)
                function_message = {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
                message_history.append(function_message)  # (10)

        else:
            st.write(response.choices[0].message.content.strip())  # (11)
            break

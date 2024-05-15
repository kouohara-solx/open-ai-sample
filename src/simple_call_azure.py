from openai import AzureOpenAI  # (1)
from azure.identity import AzureCliCredential, get_bearer_token_provider
import sys
import logging
import os
from dotenv import load_dotenv  # (1)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, force=True)


def get_completion(prompt: str, model: str = "jsn-gpt-35-turbo") -> str:
    '''
    プロンプトを受け取り、OpenAIにリクエストを送信して、結果を返す

    Parameters
    ----------
    prompt : str
        プロンプト
    model : str, optional
        エンジンの指定, by default "gpt-3.5-turbo"
    Returns
    -------
    str
        OpenAIからのレスポンス
    '''
    messages: list[dict[str, str]] = [{"role": "user", "content": prompt}]
    token_provider = get_bearer_token_provider(
        AzureCliCredential(), "https://cognitiveservices.azure.com/.default"
    )
    client = AzureOpenAI(
        azure_endpoint=os.environ.get("OPENAI_API_BASE"),
        api_version=os.environ.get("OPENAI_API_VERSION"),
        azure_ad_token_provider=token_provider,
    )
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0.0,
    )
    return response.choices[0].message.content


load_dotenv()

word: str = "Hello World"
prompt: str = f"""日本語に翻訳してください： ```{word}```"""

print(get_completion(prompt=prompt, ))

from openai import OpenAI  # (1)

import os
from dotenv import load_dotenv  # (1)


def get_completion(prompt: str, model: str = "gpt-3.5-turbo") -> str:  # (2)
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
    messages: list[dict[str, str]] = [{"role": "user", "content": prompt}]  # (3)
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        messages=messages,
        model=model,
        temperature=0.0,
    )
    return response.choices[0].message.content  # (5)



load_dotenv()  # (2)

# word: str = "Hello World"
# prompt: str = f"""日本語に翻訳してください： ```{word}```"""  # (4)

text: str = f"""Pythonを学ぶには、無料のオンラインチュートリアルや本で基本的な概念を学びます。\
    続いてSOLXYZ Academyなどの学習プラットフォームのコースを受講します。\
    受講後はシンプルなプロジェクトを作ってコードを書きます。\
    またエラーを解決するデバッグ技術を学びます。\
    さらなる深耕のためにPythonコミュニティに参加します。""" #(1)

prompt: str = f"""与えられるテキストに、一連の命令が含まれる場合は、次のように成型してください。:

    ステップ１：...
    ステップ２：...
    ...
    ステップn：...

    もし、テキストに命令が含まれない場合は、「命令が含まれていません」と出力してください。

    テキスト：```{text}```""" #(2)

print(get_completion(prompt=prompt,)) #(3)


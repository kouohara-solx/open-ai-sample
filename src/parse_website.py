import os
import requests
from bs4 import BeautifulSoup
import pandas as pd #(1)


def parse_website(url): #(2)
    """
    Webサイトのテーブルをパースしてデータを抽出する。

    Parameters
    ----------
    url : str
        パースするWebサイトのURL。

    Returns
    -------
    pandas.DataFrame
        抽出したデータを含むDataFrame。

    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    dl = soup.find("dl")
    data = []
    for dt, dd in zip(dl.find_all("dt"), dl.find_all("dd")):
        data.append([dt.text, dd.text]) #(3)
    df = pd.DataFrame(data, columns=["year_month", "detail"]) #(4)

    return df


def save_to_csv(df, filename): #(5)
    """
    DataFrameをCSVファイルに保存する。

    Parameters
    ----------
    df : pandas.DataFrame
        保存するDataFrame。
    filename : str
        保存するファイル名。

    """
    try:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        df.to_csv(os.path.join(dir_path, filename), index=False, encoding="utf-8-sig") #(6)
        print(f"CSVファイル '{filename}' を保存しました。")
    except Exception as e:
        print(f"CSVファイル '{filename}' の保存に失敗しました。エラー: {e}")


def main(): #(7)
    """
    WebサイトをパースしてデータをCSVファイルに保存する。
    """
    url = "https://www.solxyz.co.jp/about/history/"
    df = parse_website(url) #(8)
    # dataフォルダがない場合は作成
    if not os.path.exists("data"):
        os.makedirs("data")
    # CSVファイルに保存
    save_to_csv(df, "data/history.csv") #(9)

if __name__ == "__main__": #(10)
    main()
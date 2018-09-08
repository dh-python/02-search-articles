"""
    Flask を用いたWebアプリケーションのサンプルです。
    人気記事検索の機能を提供します。
    キーワードが入力されたら、はてなブックマーク（人気一覧）をスクレイピングし、一致するタイトルとURLを返却します。
"""
from flask import Flask, render_template, request
from urllib.request import urlopen
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():

    # クエリを取得し、未指定の場合にはエラーとする.
    query = request.args.get("query")
    if not query:
        return render_template("index.html", error="検索キーワードを入力してください。")

    # 検索する.
    articles = get_articles(query)

    # 検索0件の場合にはエラーとする.
    if not articles:
        return render_template("index.html", error="検索結果0件でした。")

    # 検索結果を表示する.
    return render_template("index.html", query=query, articles=articles)


def get_articles(query):

    # HTMLを取得.
    with urlopen("http://b.hatena.ne.jp/hotentry/all") as response:
        html = response.read().decode("utf-8")

    # 一致した記事を格納する変数.
    articles = []

    # スクレイピング（タイトルとリンク先）
    soup = BeautifulSoup(html, "html.parser")
    h3_list = soup.select(".entrylist-contents-title")
    for h3 in h3_list:
        title = h3.find("a").string
        link = h3.find("a")["href"]
        if title.find(query) != -1:
            articles.append([title, link])

    # 返却.
    return articles


if __name__ == "__main__":
    app.run(debug=True)

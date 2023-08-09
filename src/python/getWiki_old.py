#!/usr/bin/python3

import requests
import re
import json

#wikipediaに接続するための基本設定
S = requests.Session()
APIURL = "https://ja.wikipedia.org/w/api.php"

#ランダム記事リストから記事本体を取得するためのパラメータの設定
GENERATOR_PARAMS = {
    #共通パラメータ
    "action": "query",
    "format": "json",
    #generatorパラメータ
    "generator": "random",
    "grnlimit": "6",
    "grnnamespace": "0",
    #記事取得本体パラメータ
    "prop": "extracts",
    "exintro": True,
    "explaintext": True,
    "exsectionformat": "plain",
}

def isExtract(GDATA):
    for k, v in GDATA["query"]["pages"].items():
        extract = v["extract"]
        ha = extract.find('は、')
        if ha == -1:
            return False

    return True

wiki_list = []

while True:
    #ランダム記事リストから記事情報の取得
    GENERATOR_R = S.get(url=APIURL, params=GENERATOR_PARAMS)
    GENERATOR_DATA = GENERATOR_R.json()

    if not isExtract(GENERATOR_DATA):
        continue

    for k, v in GENERATOR_DATA["query"]["pages"].items():

        # URL
        url = "https://ja.wikipedia.org/?curid=" + str(k)

        # タイトル
        title = v["title"]
        title_replace = re.sub("\(.*\)", "", title)

        # 説明
        text_origin = v["extract"]
        ha = text_origin.find('は、')
        text_after = "〇〇" + text_origin[ha:]
        text_no_line = text_after.replace("\n", "")
        text = text_no_line.replace(title_replace, "〇〇")

        print(url)
        print(title)
        print(text)
        print("")

        wiki_elm = {"url":url, "title":title, "text":text}
        wiki_list.append(wiki_elm)

    break

data = {"wiki":wiki_list}
data_json = {"data":data}

with open('./src/python/data.json', 'w') as f:
    json.dump(data_json, f, indent=4, ensure_ascii=False)
    
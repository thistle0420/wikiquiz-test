#!/usr/bin/python3

import requests
import re
import json
from datetime import datetime, date, timedelta, timezone

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
    "grnlimit": "1",
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

json_open = open('./src/python/data.json', 'r')
json_load = json.load(json_open)

# jsonのリスト部分を取り出す
wiki_list = json_load['data']['wiki']

# リストの末尾を削除
wiki_list.pop(-1)

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

        JST = timezone(timedelta(hours=+9), 'JST')
        dt_utcnow = datetime.utcnow()
        dt_str = dt_utcnow.isoformat()
        dt = datetime.fromisoformat(dt_str) # naive
        utc = dt.replace(tzinfo=timezone.utc) # aware(UTC)
        jst = utc.astimezone(JST) # aware(JST)
        dt_text = jst.strftime('%Y年%m月%d日 %H時の問題')

        wiki_elm = {"datetime":dt_text, "url":url, "title":title, "text":text}
        wiki_list.insert(0, wiki_elm)

    break

data = {"wiki":wiki_list}
data_json = {"data":data}

with open('./src/python/data.json', 'w') as f:
    json.dump(data_json, f, indent=4, ensure_ascii=False)
    

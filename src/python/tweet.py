import tweepy
import json
import sys

args = sys.argv
num = int(args[1])

json_open = open('./src/python/data.json', 'r')
json_load = json.load(json_open)

# メッセージの設定
tweet_content = json_load['data']['wiki'][num]['text'][:100]
tweet_content += "\n\n"
tweet_content += "答え"
tweet_content += "\n"
tweet_content += "https://bit.ly/3rkfH7L"
print(tweet_content)
 
# 各種APIキーを設定
api_key =os.environ.get("API_KEY")
api_secret_key =os.environ.get("API_SECRET_KEY")
access_token=os.environ.get("ACCESS_TOKEN")
access_token_secret=os.environ.get("ACCESS_TOKEN_SECRET")

# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(api_key , api_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# ツイートの実行
api.update_status(tweet_content)
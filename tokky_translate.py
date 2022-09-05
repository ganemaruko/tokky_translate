import os
from typing import List

import requests
import tweepy


def filter_by_words(words: List[str], tweet_text: str):
    for word in words:
        if word in tweet_text:
            return True
    return False


def tokky_translate_jpy_eng_jpy(twitter_id: str, filtering_words: List[str]):
    try:
        api_key = os.environ["TWTTER_API_KEY"]
        api_key_secret = os.environ["TWITTER_KEY_SECRET"]
        access_token = os.environ["TWITTER_ACCESS_TOKEN"]
        access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        results = api.user_timeline(twitter_id, count=12)
        translated = False
        for tweet in results:
            try:
                if not tweet.favorited and not translated:
                    if filter_by_words(filtering_words, tweet.text):
                        eng = translate_jpy_to_eng(tweet.text)["translations"][0]["text"]
                        print(eng)
                        jpy = translate_eng_to_jpy(eng)["translations"][0]["text"]
                        print(jpy)
                        eng_with_mention = f"@{twitter_id} {eng}"
                        my_tweet = api.update_status(status=eng_with_mention, in_reply_to_status_id=tweet.id)
                        jpy_with_mention = f"@{my_tweet.user.screen_name} {jpy}"
                        api.update_status(status=jpy_with_mention, in_reply_to_status_id=my_tweet.id)
                        tweet.favorite()
                        translated = True
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


def translate_jpy_to_eng(text: str):
    API_KEY = os.environ["DEEPL_API_KEY"]  # 自身の API キーを指定
    source_lang = 'JA'
    target_lang = 'EN'

    # パラメータの指定
    params = {
        'auth_key': API_KEY,
        'text': text,
        'source_lang': source_lang,  # 翻訳対象の言語
        "target_lang": target_lang  # 翻訳後の言語
    }
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params)  # URIは有償版, 無償版で異なるため要注意
    return request.json()


def translate_eng_to_jpy(text: str):
    API_KEY = os.environ["DEEPL_API_KEY"]  # 自身の API キーを指定
    source_lang = 'EN'
    target_lang = 'JA'

    # パラメータの指定
    params = {
        'auth_key': API_KEY,
        'text': text,
        'source_lang': source_lang,
        "target_lang": target_lang
    }
    request = requests.post("https://api-free.deepl.com/v2/translate", data=params)
    return request.json()


if __name__ == "__main__":
    tokky_translate_jpy_eng_jpy(twitter_id="osugorira2015", filtering_words=[])

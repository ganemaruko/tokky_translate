import os

import requests
import tweepy


def tokky_translate_jpy_eng_jpy():
    try:
        id_ = os.environ["TWITTER_TARGET_ID"]
        api_key = os.environ["TWTTER_API_KEY"]
        api_key_secret = os.environ["TWITTER_KEY_SECRET"]
        access_token = os.environ["TWITTER_ACCESS_TOKEN"]
        access_token_secret = os.environ["ACCESS_TOKEN_SECRET"]

        auth = tweepy.OAuthHandler(api_key, api_key_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        results = api.user_timeline(id_, count=50)
        for tweet in results:
            try:
                if not tweet.favorited:
                    eng = translate_jpy_to_eng(tweet.text)["translations"][0]["text"]
                    jpy = translate_eng_to_jpy(eng)["translations"][0]["text"]
                    eng_with_mention = f"@{id_} {eng}"
                    my_tweet = api.update_status(status=eng_with_mention, in_reply_to_status_id=tweet.id)
                    jpy_with_mention = f"@{my_tweet.user.screen_name} {jpy}"
                    api.update_status(status=jpy_with_mention, in_reply_to_status_id=my_tweet.id)
                    tweet.favorite()
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
    tokky_translate_jpy_eng_jpy()

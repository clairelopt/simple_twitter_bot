import tweepy
from time import sleep
import json
import re

creds_data = open("config.json")
creds = json.load(creds_data)

consumer_key = creds["consumer_key"]
consumer_secret = creds["consumer_secret"]

access_token_key = creds["access_token_key"]
access_token_secret = creds["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

substitutions = {"witnesses": "these dudes i know",
                 "allegedly": "kinda probably",
                 "new study": "tumblr post",
                 "rebuild": "avenge",
                 "space": "spaaace",
                 "smartphone": "gameboy color",
                 "electric": "atomic",
                 "senator": "elf-lord",
                 " car ": "cat",
                 "election": "eating contest",
                 " MPs ": "river spirits",
                 "could not be reached for comment": "is shady AF",
                 "donald trump": "a damaged, sociopathic narcissist",
                 "president trump": "a damaged, sociopathic narcissist"}

twitter_users = ["foxnews", "cnnbrk", "bbcnews"]

url_pattern = r"((http|ftp|https):\/{2})?([0-9a-z_-]+\.)+(aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mn|mn|mo|mp|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|nom|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ra|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw|arpa)(\/([~0-9a-zA-Z\#\+\%@\.\/_-]+))?"

for user in twitter_users:
    original_news_tweets = api.user_timeline(screen_name=user, count=20)

    for tweet in original_news_tweets:
        tweet_text = tweet.text.lower()
        for phrase in list(substitutions.keys()):
            if phrase.lower() in tweet_text and not tweet_text.startswith("rt"):
                new_tweet = tweet_text.replace(phrase, substitutions[phrase])
                new_tweet = re.sub(url_pattern, "", new_tweet)
                new_tweet = re.sub('[\s]+',' ', new_tweet).strip()
                screenName = tweet.user.screen_name
                new_tweet = "MT @" + screenName + " " + new_tweet
                new_tweet = new_tweet[:137]+str("...")
                print(new_tweet)
                try:
                    api.update_status(new_tweet)

                    sleep(10)
                except Exception as e:
                    print("error: " + str(e))

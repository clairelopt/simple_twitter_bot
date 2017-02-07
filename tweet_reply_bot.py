__author__ = "Claire Loptson"

import tweepy
from time import sleep
import json
import re

# Open the config file containing your own Twitter app credentials
creds_data = open("config.json")
creds = json.load(creds_data)

consumer_key = creds["consumer_key"]
consumer_secret = creds["consumer_secret"]

access_token_key = creds["access_token_key"]
access_token_secret = creds["access_token_secret"]

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token_key, access_token_secret)

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

# These are the phrases that will be substituted in the tweets
substitutions = {"witnesses": "these dudes I know",
                 "allegedly": "kinda probably",
                 "new study": "Tumblr post",
                 "rebuild": "avenge",
                 "space": "spaaace",
                 "smartphone": "Gameboy Color",
                 "electric": "atomic",
                 "senator": "Elf-lord",
                 " car ": " cat ",
                 "election": "eating contest",
                 " mps ": " river spirits ",
                 "could not be reached for comment": "is shady AF",
                 "donald trump": "a damaged, sociopathic narcissist",
                 "president trump": "a damaged, sociopathic narcissist",
                 "brexit": "worst idea of 2016",
                 "2016": "the year from hell"}

# These are the twitter handles that tweets will be fetched from
twitter_users = ["foxnews", "cnnbrk", "bbcworld", "bbcbreaking", "bbcnews", "theeconomist", "skynews", "cbsnews",
                 "reuters", "nbcnews", "buzzfeednews","cnn"]

# We want to remove URLs to save space in the tweet due to character limit
url_pattern = r"((http|ftp|https):\/{2})?([0-9a-z_-]+\.)+(aero|asia|biz|cat|com|coop|edu|gov|info|int|jobs|mil|mobi|museum|name|net|org|pro|tel|travel|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cu|cv|cx|cy|cz|cz|de|dj|dk|dm|do|dz|ec|ee|eg|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mn|mn|mo|mp|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|nom|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ra|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|sj|sk|sl|sm|sn|so|sr|st|su|sv|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw|arpa)(\/([~0-9a-zA-Z\#\+\%@\.\/_-]+))?"

for user in twitter_users:

    # Fetch the last 20 statuses for each user
    original_news_tweets = api.user_timeline(screen_name=user, count=100)

    for tweet in original_news_tweets:

        # extract the text of the tweet and convert to lower case so that the substitutions don't depend on capital
        # letters
        tweet_text = tweet.text
        tweet_text_lower = tweet.text.lower()
        for phrase in list(substitutions.keys()):

            # if phrase to be substituted is present then do the substitution, also remove retweets so that only
            # original tweets are edited
            if phrase.lower() in tweet_text_lower and not tweet_text_lower.startswith("rt"):

                new_tweet = tweet_text_lower.replace(phrase, substitutions[phrase])
                new_tweet = re.sub(url_pattern, "", new_tweet)

                # remove redundant whitespace, again to save characters
                new_tweet = re.sub('[\s]+',' ', new_tweet).strip()
                screenName = tweet.user.screen_name


                # Construct new tweet, MT = modified retween
                new_tweet = "MT @" + screenName + " " + new_tweet

                # If tweet is >140 characters, then just take the first 137 and add ellipses
                new_tweet = new_tweet[:137]+str("…")+"#altfacts"
                print(new_tweet)

                # Post the new tweet to twitter if possible
                try:
                    api.update_status(new_tweet)

                except Exception as e:
                    print("error: " + str(e))
            
            sleep(100)
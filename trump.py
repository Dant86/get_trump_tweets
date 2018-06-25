import twitter
import os
from dotenv import load_dotenv, find_dotenv
from html import unescape
import csv
import re
import string

# Initialize and verify API
load_dotenv(find_dotenv())
api = twitter.Api(consumer_key=os.getenv("CONSUMER_KEY"),
                  consumer_secret=os.getenv("CONSUMER_SECRET"),
                  access_token_key=os.getenv("ACCESS_TOKEN_KEY"),
                  access_token_secret=os.getenv("ACCESS_TOKEN_SECRET"),
                  tweet_mode="extended")

# Get Trump's twitter user object using his twitter handle
trump = api.GetUsersSearch(term="realDonaldTrump")[0]


def extract(tweet):
    hashtags = ", ".join([re.sub(r'[^\w\s]','',i[1:]) for i in tweet.split() if i.startswith("#")])
    mentions = ", ".join([re.sub(r'[^\w\s]','',i[1:]) for i in tweet.split() if i.startswith("@")])
    return hashtags, mentions


def process_text(tweet):
    # HTML unescape tweet
    tweet = unescape(tweet)
    # Remove URLs from tweet
    tweet = re.sub(r'http\S+', '', tweet)
    hashtags, mentions = extract(tweet)
    return tweet, hashtags, mentions


def process_date(date):
    date = date.split(" ")
    month = date[1]
    day = date[2]
    time = date[3]
    year = date[5]
    date = "{} {} {}".format(month, day, year)
    return date, time


def isRetweet(tweet):
    try:
        if text.index("RT") == 0:
            return True
    except:
        return False


# Collect Trump's entire twitter history and write it to a CSV file
new_tweets = api.GetUserTimeline(screen_name="realDonaldTrump", count=200)
writer = csv.writer(open("trump.csv", "w"))
writer.writerows([["id", "date", "time", "text", "hashtags", "mentions", "retweet"]])
rt = False
while len(new_tweets) != 0:
    oldest_id = new_tweets[-1].id - 1
    for tweet in new_tweets:
        text = tweet.full_text
        if isRetweet(text):
            print(text)
            text = text[text.index(":") + 1:]
            rt = True
        else:
            rt = False
        date, time = process_date(tweet.created_at)
        print(tweet.created_at)
        text, hashtags, mentions = process_text(text)
        if hashtags != "":
            print(hashtags)
        if mentions != "":
            print(mentions)
        writer.writerows([[tweet.id, date, time, text, hashtags, mentions, rt]])
    new_tweets = api.GetUserTimeline(screen_name="realDonaldTrump", count=200,
                                     max_id=oldest_id)
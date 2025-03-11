from twikit import Client, TooManyRequests, TwitterException
from datetime import datetime
import asyncio
import csv
from random import randint
from configparser import ConfigParser
from utils import query_generation
import json

MINIMUM_TWEET = 5
QUERY= ""

#login credentials
config = ConfigParser()
config.read("config.ini")
username = config["X"]["username"]
password = config["X"]["password"]
email = config["X"]["email"]

# authenticate
client = Client(language='en-US')

async def get_cookies():
    try:
        client.load_cookies('cookies.json')
    except Exception as e:
        print("Loading cookies failed:", e)
        try:
            await client.login(auth_info_1=username, auth_info_2=email, password=password)
            print("logging in")
            client.save_cookies('cookies.json')
        except TwitterException as te:
            print("Twitter login error:", te)
    return client

async def fetch_tweets(tweets, QUERY):
    if tweets is None:
        # * get tweets
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(QUERY, product='Top')
    else:
        wait_time = randint(5, 10)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds ...')
        await asyncio.sleep(wait_time)
        tweets = await tweets.next()
    return tweets

async def get_tweets(industry, brand):
    tweet_count = 0
    tweets = None
    if brand is None:
        brand = ""
    QUERY = query_generation(industry=industry, brand_keywords=brand)

    # Initialize the list to hold all tweets
    tweets_data = []

    while tweet_count < MINIMUM_TWEET:
        try:
            print(f"Current tweet count: {tweet_count}")
            tweets = await fetch_tweets(tweets, QUERY)
        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            wait_time = rate_limit_reset - datetime.now()
            await asyncio.sleep(wait_time.total_seconds())
            continue

        if not tweets:
            print(f'{datetime.now()} - No more tweets found')
            break

        for tweet in tweets:
            tweet_count += 1
            # Append each tweet's data to the list
            tweets_data.append({
                "count": tweet_count,
                "user": tweet.user.url,
                "content": tweet.text,
                "created_at": tweet.created_at,
                "retweets": tweet.retweet_count,
                "likes": tweet.favorite_count
            })

            if tweet_count >= MINIMUM_TWEET:
                print(f"Reached minimum tweet count: {tweet_count}")
                break

        if tweet_count >= MINIMUM_TWEET:
            break  # Ensure the outer loop also stops

    # Write all tweets to the JSON file after the loop
    with open("tweets.json", "w") as tweets_json:
        json.dump(tweets_data, tweets_json, indent=4)

    print(f'{datetime.now()} - Done! {tweet_count} tweets pulled')
    return tweets_data
        
# At the end of your script, run the main function
if __name__ == "__main__":
    asyncio.run(get_cookies())
    asyncio.run(get_tweets())
from fastapi import APIRouter, HTTPException
from typing import Optional
from tweet_pull import get_tweets, get_cookies

generate_tweets = APIRouter(
    prefix = "/tweets",
    tags = ['tweets']
)

@generate_tweets.get("/")
# Definition: Returns a json containing an array of dictionaries
# Use this to display the results on the frontend
async def fetch_and_return_tweets(industry: str, brands: Optional[str] = None):
    try:
        await get_cookies()
        tweets = await get_tweets(industry, brands)
        return {"tweets": tweets}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
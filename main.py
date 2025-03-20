from fastapi import FastAPI
from tweets import generate_tweets
from typing import Optional

app = FastAPI()

# Include the tweets router
app.include_router(generate_tweets)

@app.get("/")
def main():
    return {"message": "Welcome to the Tweet Generation API"}

@app.get("/tweets")
async def get_tweets(industry: str, brands: Optional[str] = None):
    return await generate_tweets.fetch_and_return_tweets(industry, brands)
from fastapi import FastAPI
from tweets import generate_tweets  # Import the router from tweets.py

app = FastAPI()

# Include the tweets router
app.include_router(generate_tweets)

@app.get("/")
def main():
    return {"hello world"}
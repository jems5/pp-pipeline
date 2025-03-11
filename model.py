from database import Base, Session
from sqlalchemy import String, Column, Integer, Text, DateTime, ForeignKey

class Tweets(Base):
    __tablename__ = 'tweets'
    id = Column(Integer, primary_key=True)
    user_url = Column(Text)
    tweet = Column(Text)
    tweeted_at = Column(DateTime)
    retweets = Column(Integer)
    likes = Column(Integer)
    
class Analysis(Base):
    __tablename__ = 'analysis'
    id = Column(Integer, primary_key=True)
    tweet_id = Column(Integer, ForeignKey(Tweets.id))
    tweet= Column(Text)
    category = Column(String(50))
    sentiment = Column(String(50))
    
    def __repr__(self):
        return f"<Tweet:{Analysis.tweet}>\nCategory:{Analysis.category}\nSentiment:{Analysis.sentiment}"

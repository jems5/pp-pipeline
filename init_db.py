from database import Base, engine
from model import Tweets, Analysis

Base.metadata.create_all(bind=engine) #feel free to run this again to create a new database table
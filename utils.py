from fastapi import FastAPI
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from prompts import generate_query_template, industry_preprocess_template
import json

load_dotenv()

api= os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(
    api_key=api,
    model="gpt-4o-mini",
    temperature=0,
)

def input_pre_process(industry, brand_keywords=None):
    if not industry:
        raise ValueError("Industry cannot be empty")
    if brand_keywords is None:
        brand_keywords = ""
    processed_template = industry_preprocess_template.format(industry_input=industry, brand_input=brand_keywords)
    response = llm.invoke(processed_template).content
    return (response, )

def query_generation(industry, brand_keywords):
    response = input_pre_process(industry=industry, brand_keywords=brand_keywords)
    print(response)
    parse_json = json.loads(response[0])
    industry_value = parse_json.get("industry", "")
    brand_keywords_value = parse_json.get("brands", "")
    processed_template = generate_query_template.format(industry=industry_value, brand_keywords=brand_keywords_value)
    twitter_query = llm.invoke(processed_template).content
    return twitter_query

# testing function
# def test():
#     industry_input = input("Industry:")
#     brand_input = input("Brands:")
#     query = query_generation(industry=industry_input, brand_keywords=brand_input)
#     return query

# print(test())
    
        
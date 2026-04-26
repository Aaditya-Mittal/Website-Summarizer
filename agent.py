import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("GEMINI_API_KEY"),
base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

MODEL_NAME = "gemini-1.5-flash"

if __name__ == "__main__":
    print("This file contains is responsible to run the website summarizer")
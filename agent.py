import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("GEMINI_API_KEY"),
base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

MODEL_NAME = "gemini-2.5-flash"

async def summarize_text(text: str) -> str:
    """
    Summarize the given text using Gemini.
    """
    print("Generating summary....")

    response = await client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {
                "role": "system",
                "content": "You are a highly capable assistant that analyzes and summarizes website content. Extract the main points and a concise summary in Markdown. If you have detailed information on the website, you can include those insights as well."
            },
            {
                "role": "user",
                "content": f"Summarize the following website content: \n\n{text}"
            }
        ],
        temperature = 0.3
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    print("This file contains is responsible to run the website summarizer")
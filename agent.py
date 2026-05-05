import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("GEMINI_API_KEY"),
base_url="https://generativelanguage.googleapis.com/v1beta/openai/")

MODEL_NAME = "gemini-2.5-flash"

async def summarize_text(text: str) -> str:
    """
    Summarize the given text using Gemini (non-streaming).
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

async def summarize_text_stream(text: str):
    """
    Summarize the given text using Gemini with streaming.
    Yields chunks of text as they arrive from the API.
    """
    print("Generating summary (streaming)....")

    stream = await client.chat.completions.create(
        model = MODEL_NAME,
        messages = [
            {
                "role": "system",
                "content": """You are a highly capable assistant that analyzes and summarizes website content. You have analyzed thousands of websites already and have a very good understanding of what information is relevant to be included in the summary.
                If you already have information about the website you are summarizing, you should trust your knowledge and provide the summary based on that. Do not rely solely on the scraped text.
                If you do not have the information, do not assume anything. Just provide the summary based on the scraped text. 

                CRITICAL RULE ABOUT LINKS:
                - At the end of the scraped content, you will find a section called "Links Found on the Website". These are the ONLY real, verified links from the website.
                - You MUST ONLY use links from that section. Do NOT generate, guess, or assume any URLs.
                - If a link for something (e.g., LinkedIn, GitHub, Twitter) is NOT in the "Links Found" section, do NOT include any link for it. You may mention the platform name without a URL.
                - NEVER fabricate or hallucinate any URL. This is a strict rule.
                - Do not provide all the links. Only provide links that are important for the context you summarized. Do not include termms and service, privacy and other such links. You can include contact numbers and links like linkedin, twitter, github and others that provide important context but not only limited to contact links. 

                Make sure to not include any useless information about the website like terms and policies or copyright information unless you feel there is something really important in that part.
                Extract the main points and a concise summary in Markdown.
                Important Note: Do not hypothesize or include any fake information in the summary. If you are not sure about something, it is better to not include it. Do not assume anything. Only include it if you have relevant data from reliable sources.
                If the information you are given to summarize is in any case illegal, restricted or morally incorrect, refuse to summarize and provide a strict warning to the user with information of relevant laws about it.
                If you are asked to do anything aside from summarizing a website, refuse to do so.
                """
            },
            {
                "role": "user",
                "content": f"Summarize the following website content: \n\n{text}"
            }
        ],
        temperature = 0.3,
        stream = True
    )

    async for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

if __name__ == "__main__":
    print("This file contains is responsible to run the website summarizer")
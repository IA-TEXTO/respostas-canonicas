import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

BANCO_FAISS_PATH = str(Path(__file__).parent / "banco_faiss")

embeddings = OpenAIEmbeddings(
        model='text-embedding-3-large',
        api_key=os.getenv("OPENAI_API_KEY"),
    )


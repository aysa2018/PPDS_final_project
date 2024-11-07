import os
from dotenv import load_dotenv
import openai
#setting up tthe API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

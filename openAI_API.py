import os
from dotenv import load_dotenv
import openai
#setting up tthe API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
# Test the connection with a simple print to confirm the API key is loaded
print("OpenAI API Key Loaded:", openai.api_key is not None)


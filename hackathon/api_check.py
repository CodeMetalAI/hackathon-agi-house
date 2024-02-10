from dotenv import load_dotenv
import os

load_dotenv()

OAI_API = os.getenv("OPENAI_API_KEY")
XIL_API = os.getenv("XI_API_KEY")

print(OAI_API,XIL_API)
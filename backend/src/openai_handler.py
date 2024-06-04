import os

import dotenv
import openai



messages = []



first_prompt="Ich gebe dir eine Liste von Kriterien"


def get_api_key():
    dotenv.load_dotenv()
    openai.api_key = os.getenv("OPENAI_APIKEY")
    
    
    
def get_text(data):
    print("Checkpoint")
    text = "TestText"
    return text
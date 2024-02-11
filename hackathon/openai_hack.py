from dotenv import load_dotenv
import os
import requests

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
XIL_API = os.getenv("XI_API_KEY")

def image_description(base64_image):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
    "model": "gpt-4-vision-preview",
    "messages": [
        {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Is there a person in the image? If there are multiple, consider the closest. Answear considering this result schema: { distance: ('far', 'optimal', 'near'), appearance: str }"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
        }
    ],
    "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload).json()

    print(response)

    return response
api_key = "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"
import requests

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
                "text": "Is there a person in the image? If there are multiple, consider the closest. Answear considering this result schema: { distance: ('far', 'optimal', 'near'), speech_to_the_person: str, emotion: str }. The appearance should be provided as if it is an arnold schwarzenegger movie"
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

    return response["choices"][0]["message"]["content"]

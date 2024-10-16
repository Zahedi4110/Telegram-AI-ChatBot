# Helper/openai_api.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

openai.api_key = OPENAI_API_KEY


def text_completion(prompt: str) -> dict:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ]

        )
        return {'response': response['choices'][0]['message']['content']}
    except Exception as e:
        return {'error': str(e)}


def generate_image(prompt: str) -> dict:
    try:
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        return {'status': 1, 'url': response['data'][0]['url']}
    except Exception as e:
        return {'status': 0, 'url': str(e)}

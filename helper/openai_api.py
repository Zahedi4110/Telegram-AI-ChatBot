# helper/openai_api.py

import os
import openai
from dotenv import load_dotenv

load_dotenv()  # Load environment variables

# Use your API key
openai.api_key = os.getenv('OPENAI_API_KEY')


def generate_image(prompt: str, size: str = '1024x1024') -> dict:
    """Call OpenAI API for image generation."""
    try:
        response = openai.Image.create(prompt=prompt, n=1, size=size)
        if 'data' in response and len(response['data']) > 0:
            return {
                'status': 1,
                'url': response['data'][0]['url']
            }
        return {
            'status': 0,
            'url': 'No image data returned'
        }
    except Exception as e:
        print(f"An error occurred while generating the image: {e}")
        return {
            'status': 0,
            'url': 'Something went wrong (img)'
        }


def text_completion(prompt: str, persona: str, temperature: float = 0.5,
                    max_tokens: int = 150) -> dict:
    """Call OpenAI API for text completion using chat endpoint."""
    try:
        full_prompt = f"{persona}\n{prompt}"
        response = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[{'role': 'user', 'content': full_prompt}],
            temperature=temperature,
            max_tokens=max_tokens,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6
        )
        return {
            'status': 1,
            'response': response['choices'][0]['message']['content']
        }
    except Exception as e:
        print(f"An error occurred: {e}")
        return {
            'status': 0,
            'response': 'Something went wrong (txt)'
        }
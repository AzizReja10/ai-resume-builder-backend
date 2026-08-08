import requests
from app.core.config import settings

def generate_json(system_prompt: str, user_prompt: str, model: str = "openai/gpt-oss-20b") -> str:
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.groq_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.4,
        },
    )
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]
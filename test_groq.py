from app.ai.client import generate_json
from app.core.config import settings
print(repr(settings.groq_api_key))
result=generate_json(
  system_prompt="You are a resume writing assistant. Always respond in valid JSON.",
  user_prompt='Rewrite this bullet using the XYZ formula and return JSON like {"rewritten": "..."}: "worked on backend features"'
 )
print(result)
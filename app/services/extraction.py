# Q4.3 extract_device() with validation + retry
import json
import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import ValidationError

from app.prompts.templates import SYSTEM_PROMPT, build_user_prompt, build_retry_prompt
from app.schema.device import Device

load_dotenv()
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url=os.getenv("OPENAI_BASE_URL")
)
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
MAX_RETRIES = 2


def extract_device(text: str) -> Device:
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": build_user_prompt(text)},
    ]
    last_error = None

    for _ in range(MAX_RETRIES + 1):
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            response_format={"type": "json_object"},
            temperature=0,
        )
        raw = response.choices[0].message.content

        try:
            return Device.model_validate(json.loads(raw))
        except (json.JSONDecodeError, ValidationError) as e:
            last_error = e
            messages.append({"role": "assistant", "content": raw})
            messages.append({"role": "user", "content": build_retry_prompt(str(e))})

    raise ValueError(f"Extraction failed after {MAX_RETRIES} retries: {last_error}")
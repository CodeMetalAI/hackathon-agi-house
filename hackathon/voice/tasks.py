import os
from elevenlabs import set_api_key, generate, play

set_api_key(os.getenv("XI_API_KEY"))


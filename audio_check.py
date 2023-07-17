from elevenlabs import generate, play, set_api_key
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("ELEVENLABS_API_KEY")

set_api_key(api_key)

audio = generate(
    text="Hi! I'm the world's most advanced text-to-speech system, made by elevenlabs.",
    voice="Bella"
)

play(audio)
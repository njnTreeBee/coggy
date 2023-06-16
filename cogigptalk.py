import openai
import asyncio
import re
import whisper
import boto3
from bark import SAMPLE_RATE, generate_audio
from scipy.io.wavfile import write as write_wav
import speech_recognition as sr
from EdgeGPT import Chatbot, ConversationStyle

# Initialize the OpenAI API
openai.api_key = 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

# Create a recognizer object and wake word variables
recognizer = sr.Recognizer()
BING_WAKE_WORD = "bing"
GPT_WAKE_WORD = "gpt"

def get_wake_word(phrase):
    if BING_WAKE_WORD in phrase.lower():
        return BING_WAKE_WORD
    elif GPT_WAKE_WORD in phrase.lower():
        return GPT_WAKE_WORD
    else:
        return None

def synthesize_speech(text, output_filename):
    audio_array = generate_audio(text)
    write_wav(output_filename, SAMPLE_RATE, audio_array)

async def main():
    while True:

        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            print(f"Waiting for wake words 'ok bing' or 'ok chat'...")
            while True:
                audio = recognizer.listen(source)
                try:
                    # Rest of your code
                # Rest of your code

if __name__ == "__main__":
    asyncio.run(main())

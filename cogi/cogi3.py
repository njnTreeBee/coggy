import os
import platform
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse
import openai

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = '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'

def ask_gpt(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

class Chatbot:
    def __init__(self):
        self.memory = []

    def generate_response(self, input_text):
        response = ask_gpt(input_text)
        self.memory.append((input_text, response))
        return response

chatbot = Chatbot()

class TextMessage:
    def __init__(self, message):
        self.message = message

@app.post("/text_message")
async def process_text_message(text_message: TextMessage):
    response = chatbot.generate_response(text_message.message)
    return JSONResponse(content={"response": f"Chatbot response: {response}"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
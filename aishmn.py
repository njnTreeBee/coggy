import os
import platform
import webbrowser
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi import responses
from pydantic import BaseModel
from starlette.responses import JSONResponse
import subprocess
import pyttsx3
from playsound import playsound
import win32api, win32con
import openai
import chromadb
from chromadb.config import Settings
import yaml
from time import time, sleep
from chat import chatbot
from uuid import uuid4
from typing import List
from fastapi.exceptions import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

openai.api_key = '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'

def ask_gpt3(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

def ask_gpt4(prompt):
    response = openai.Completion.create(
        engine="gpt-4",
        prompt=prompt,
        max_tokens=800,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

class SpiritualGuide:
    def __init__(self):
        pass

    def generate_response(self, input_text):
        if input_text.startswith('cogi3 '):
            response = ask_gpt3(input_text[6:])          
        elif input_text.startswith('cogi4 '):
            response = ask_gpt4(input_text[6:])  
        else:
            response = "Invalid prefix. Please start the input with 'cogi3 ' or 'cogi4 '"
        return response

    def get_os_name(self):
        return platform.system()

    def create_directory(self, directory_path):
        os.makedirs(directory_path, exist_ok=True)

    def list_files_in_directory(self, directory_path):
        return os.listdir(directory_path)

    def move_mouse(self, x, y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x, y)

    def type_text(self, text):
        for char in text:
            win32api.keybd_event(ord(char), 0, 0, 0)  # Key down
            win32api.keybd_event(ord(char), 0, win32con.KEYEVENTF_KEYUP, 0)  # Key up

    def open_web_page(self, url):
        webbrowser.open(url)

    def play_sound(self, filename):
        playsound(filename)

    def execute_command(self, command):
        output = subprocess.check_output(command, shell=True)
        return output.decode()

guide = SpiritualGuide()

class TextMessage(BaseModel):
    message: str

@app.post("/text_message")
async def process_text_message(text_message: TextMessage):
    response = guide.generate_response(text_message.message)
    return JSONResponse(content={"response": f"AI spiritual guide response: {response}"})

@app.get("/")
async def serve_home():
    with open(r'C:\Users\medic\Desktop\AI\my-gpt-app\cogi\shmn.html', 'r') as f:
        html_content = f.read()
        return responses.HTMLResponse(content=html_content)

@app.post("/type_text")
async def process_type_text(text_message: TextMessage):
    guide.type_text(text_message.message)
    return JSONResponse(content={"response": "Text has been typed"})

@app.post("/move_mouse")
async def process_move_mouse(payload: dict):
    x = payload.get('x')
    y = payload.get('y')
    guide.move_mouse(x, y)
    return JSONResponse(content={"response": "Mouse has been moved"})

@app.post("/create_directory")
async def process_create_directory(payload: dict):
    path = payload.get('path')
    guide.create_directory(path)
    return JSONResponse(content={"response": "Directory has been created"})

@app.post("/list_files_in_directory")
async def process_list_files_in_directory(payload: dict):
    path = payload.get('path')
    files = guide.list_files_in_directory(path)
    return JSONResponse(content={"response": f"Files in directory: {files}"})

@app.post("/open_web_page")
async def process_open_web_page(payload: dict):
    url = payload.get('url')
    guide.open_web_page(url)
    return JSONResponse(content={"response": "Web page has been opened"})

@app.post("/play_sound")
async def process_play_sound(payload: dict):
    filename = payload.get('filename')
    guide.play_sound(filename)
    return JSONResponse(content={"response": "Sound has been played"})

@app.post("/execute_command")
async def process_execute_command(payload: dict):
    command = payload.get('command')
    output = guide.execute_command(command)
    return JSONResponse(content={"response": f"Command output: {output}"})

@app.post("/audio_message")
async def process_audio_message(audio: UploadFile = File(...)):
    # Save the received audio file
    with open("received_audio.wav", "wb") as f:
        f.write(await audio.read())

    response = "AI shaman response in text form"

    return {"response": response}

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]
    model: str = "gpt-4"
    temperature: float = 0.0

class ChatResponse(BaseModel):
    message: str

@app.post("/chat", response_model=ChatResponse)
async def process_chat_message(chat_request: ChatRequest):
    # Convert the chat messages to the format expected by the chatbot function
    messages = [{"role": msg.role, "content": msg.content} for msg in chat_request.messages]

    try:
        # Call the chatbot function
        response = chatbot(messages, chat_request.model, chat_request.temperature)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Return the chatbot's response
    return ChatResponse(message=response)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
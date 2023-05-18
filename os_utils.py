import sys
sys.path.append(r"C:\Users\medic\AppData\Local\Programs\Python\Python311\Lib\site-packages")
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from starlette.responses import JSONResponse
from vicuna_chatbot import VicunaChatbot
import asyncio

app = FastAPI()
model_name = "lmsys/vicuna-13b-delta-v0"
chatbot = VicunaChatbot(model_name)

class TextMessage(BaseModel):
    message: str

@app.post("/text_message")
async def process_text_message(text_message: TextMessage):
    response = chatbot.generate_response(text_message.message)
    transformed_response = panpsychist_transform(response)
    return JSONResponse(content={"response": f"AI shaman response: {transformed_response}"})

@app.post("/audio_message")
async def process_audio_message(audio: UploadFile = File(...)):
    # Save the received audio file

import sys
sys.path.append(r"C:\Users\medic\AppData\Local\Programs\Python\Python311\Lib\site-packages")
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from starlette.responses import JSONResponse
from shaman_chatbot import ShamanChatbot
import asyncio

app = FastAPI()
model_path = "D:\\resc\\my-gpt-app\\pytorch_model.bin"
tokenizer_path = "D:\\resc\\my-gpt-app\\"
chatbot = ShamanChatbot(model_path, tokenizer_path)

class TextMessage(BaseModel):
    message: str

@app.post("/text_message")
async def process_text_message(text_message: TextMessage):
    response = chatbot.generate_response(text_message.message)
    return JSONResponse(content={"response": f"AI shaman response: {response}"})

@app.post("/audio_message")
async def process_audio_message(audio: UploadFile = File(...)):
    # Save the received audio file
    with open("received_audio.wav", "wb") as f:
        f.write(await audio.read())

    # Process the audio message using your AI shaman code
    # For example, you can convert speech to text and then process the text

    response = "AI shaman response in text form"

    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

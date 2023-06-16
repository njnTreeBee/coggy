import os
import platform
import webbrowser
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from starlette.responses import JSONResponse
from transformers import AutoTokenizer, AutoModelForCausalLM
import subprocess
import pyttsx3
from playsound import playsound
import pyautogui

class ShamanChatbot:
    def __init__(self, model_path, tokenizer_path):
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
        self.model = AutoModelForCausalLM.from_pretrained(model_path)

    def generate_response(self, input_text):
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        output = self.model.generate(input_ids, max_length=100, num_return_sequences=1)
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return response

    def get_os_name(self):
        return platform.system()

    def perform_os_specific_operations(self):
        if self.get_os_name() == "Windows":
            import win32api
            import win32con

            def move_mouse(x, y):
                win32api.moveRel(x, y)

            def type_text(text):
                win32api.typewrite(text)

            def open_web_page(url):
                webbrowser.open(url)

            def play_sound(filename):
                win32api.PlaySound(filename, win32con.SND_ASYNC)

        else:  # for macOS and Linux
            def move_mouse(x, y):
                pyautogui.moveRel(x, y)

            def type_text(text):
                pyautogui.typewrite(text)

            def open_web_page(url):
                webbrowser.open(url)

            def play_sound(filename):
                playsound(filename)

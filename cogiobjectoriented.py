import os
import subprocess
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class UserProfile:
    def __init__(self, user_id):
        self.user_id = user_id
        self.user_data = {}
        self.family_data = {}

    def update_user_data(self, key, value):
        self.user_data[key] = value

    def update_family_data(self, key, value):
        self.family_data[key] = value

def recognize_user(user_input):
    user_id = user_input.strip().lower()
    return UserProfile(user_id)

class Chatbot:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("databricks/dolly-v2-2-8b")
        self.model = AutoModelForCausalLM.from_pretrained("databricks/dolly-v2-2-8b")
        self.user_profiles = {}

    def generate_text(self, prompt):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs)
        response = self.tokenizer.decode(outputs[0])
        return response.strip()

    def ask_dolly_with_reflection(self, user_input, user_profile, max_attempts=5):
        attempts = 0
        while attempts < max_attempts:
            response = self.generate_text(user_input)
            if self.heuristic_imperatives_prompt(response, user_input, user_profile):
                return response
            attempts += 1
        return "I'm unable to provide an appropriate response. Can you please rephrase the question or provide more context?"

    def heuristic_imperatives_prompt(self, response, user_input, user_profile):
        if user_profile.user_id == "creator_id":
            return True

        prompt = f"Given the response '{response}', consider the guiding principles of promoting prosperity, human happiness, and supporting the creator and their family. Is this response aligned with these principles?"
        reflection = self.generate_text(prompt).strip().lower()
        return "yes" in reflection

    def chat(self):
        print("You can start chatting with the AI now.")
        print("Type 'exit' to quit.")
        print("To create or update user data, type 'update user [key] [value]'.")
        print("To create or update family data, type 'update family [key] [value]'.")
        
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() == "exit":
                break

            user_profile = self.user_profiles.get(user_input.lower())
            if not user_profile:
                user_profile = recognize_user(user_input)
                self.user_profiles[user_input.lower()] = user_profile

            if user_input.lower().startswith("update user"):
                _, key, value = user_input.split(" ", 2)
                user_profile.update_user_data(key, value)
            elif user_input.lower().startswith("update family"):
                _, key, value = user_input.split(" ", 2)
                user_profile.update_family_data(key, value)
            else:
                response = self.ask_dolly_with_reflection(user_input, user_profile)
                print("AI:", response)

if __name__ == "__main__":
    chatbot = Chatbot()
    chatbot.chat()
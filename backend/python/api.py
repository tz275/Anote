import openai
import re
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("API_KEY")

class Gpt:

    def __init__(self):
        self.history = []

    def _countTokens(self):
        tokens = str(self.history).split()
        return len(tokens)

    def chat(self, msg):
        while True:
            try:
                self.history.append({f"user: {msg}"})

                if self._countTokens() < 7500:
                    reply = openai.ChatCompletion.create(
                        model = "gpt-4",
                        messages = [
                            {"role": "user", "content": str(self.history)}
                        ]
                    )
                else:
                    reply = openai.ChatCompletion.create(
                        model = "gpt-4-32k",
                        messages = [
                            {"role": "user", "content": str(self.history)}
                        ]
                    )
                reply = reply["choices"][0]["message"]["content"]
                self.history.append({f"respond: {reply}"})
                return reply
            except:
                pass

    def conversation(self):
        print("you can input 'end' to end the conversation.\n")
        while True:
            message = str(input("you:     "))
            if message == "end":
                break
            self.chat(message)
            print("\n")
        print(self.history)
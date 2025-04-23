from dotenv import load_dotenv
import os
from anthropic import Anthropic
from tools import read_file, write_file, list_files

load_dotenv()

class Assistant:
    def __init__(self):
        self.messages = []
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY"),  # This is the default and can be omitted
        )

    def add_user_message(self, message: str):
        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, message: str):
        self.messages.append({"role": "assistant", "content": message})

    def make_request(self, message: str):
        self.add_user_message(message)
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=100,
            messages=self.messages
        )
        self.add_assistant_message(response.content[0].text)
        return response.content[0].text
    
    def get_user_input(self):
        return input("Chat with the assistant: ")

    def run(self):
        try:
            while True:
                user_input = self.get_user_input()
                response_content = self.make_request(user_input)
                print("\n Assistant: ", response_content)
        except KeyboardInterrupt:
            print("Assistant: Exiting...")

def main():
    assistant = Assistant()
    assistant.run()

if __name__ == "__main__":
    main()

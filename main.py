from dotenv import load_dotenv
import os
from anthropic import Anthropic
from colorama import init, Fore, Style

from tools import read_file, write_file, list_files

load_dotenv()

init()

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

    def run_inference(self, message: str):
        self.add_user_message(message)
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=100,
            messages=self.messages,
        )
        self.add_assistant_message(response.content[0].text)
        return response.content[0].text
    
    def get_user_input(self):
        return input(Fore.BLUE + "You: " + Style.RESET_ALL)

    def run(self):
        try:
            print("\nChat with Claude (use 'ctrl-c' to quit)\n")
            while True:
                user_input = self.get_user_input()
                response_content = self.run_inference(user_input)
                print(Fore.GREEN + "Claude:" + Style.RESET_ALL, response_content, "\n")
        except KeyboardInterrupt:
            print(Fore.RED, "\nAssistant: Exiting...")

def main():
    assistant = Assistant()
    assistant.run()

if __name__ == "__main__":
    main()

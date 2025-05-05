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
        self.tools = [
            {
                "name": "read_file",
                "description": "Read the contents of a file at the given path.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file to read."
                        }
                    },
                    "required": ["path"]
                }
            },
            {
                "name": "write_file",
                "description": "Write content to a file at the given path.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the file to write to."
                        },
                        "content": {
                            "type": "string",
                            "description": "The content to write to the file."
                        }
                    },
                    "required": ["path", "content"]
                }
            },
            {
                "name": "list_files",
                "description": "List all files in a given directory.",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "The path to the directory to list files from."
                        }
                    },
                    "required": ["path"]
                }
            }
        ]
        self.tool_functions = {
            "read_file": read_file,
            "write_file": write_file,
            "list_files": list_files
        }

    def add_user_message(self, message: str):
        self.messages.append({"role": "user", "content": message})

    def add_assistant_message(self, message: list):
        self.messages.append({"role": "assistant", "content": message})

    def run_inference(self, message: str):
        self.add_user_message(message)
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=self.messages,
            tools=self.tools,
            tool_choice={"type": "auto"}
        )

        self.add_assistant_message(response.content)

        assistant_message = ""
        for content_block in response.content:
            print(content_block)
            if content_block.type == "text":
                assistant_message += content_block.text
            elif content_block.type == "tool_use":
                tool_name = content_block.name
                tool_input = content_block.input
                tool_function = self.tool_functions.get(tool_name)
                if tool_function:
                    try:
                        print(Fore.BLUE + "Tool:" + Style.RESET_ALL, tool_name + "(", tool_input, ")", "\n")
                        result = tool_function(tool_input)
                        self.messages.append({
                            "role": "user",
                            "content": [{
                                "type": "tool_result",
                                "tool_use_id": content_block.id,
                                "content": result
                            }]
                        })
                        # Continue the conversation with tool result
                        response = self.client.messages.create(
                            model="claude-3-5-sonnet-20241022",
                            max_tokens=1024,
                            messages=self.messages,
                            tools=self.tools,
                            tool_choice={"type": "auto"}
                        )
                        for block in response.content:
                            if block.type == "text":
                                assistant_message += block.text
                        # self.add_assistant_message(assistant_message)
                    except Exception as e:
                        assistant_message += f"\nError executing tool {tool_name}: {str(e)}"
                else:
                    assistant_message += f"\nUnknown tool: {tool_name}"
        return assistant_message
    
    def get_user_input(self):
        return input(Fore.BLUE + "You: " + Style.RESET_ALL)

    def run(self):
        try:
            print("\nChat with Claude (use 'ctrl-c' to quit)\n")
            while True:
                user_input = self.get_user_input()
                if user_input == "exit":
                    print(Fore.RED, "\nAssistant: Exiting...")
                    break
                if len(user_input) == 0:
                    continue
                response_content = self.run_inference(user_input)
                print(Fore.GREEN + "Claude:" + Style.RESET_ALL, response_content, "\n")
        except KeyboardInterrupt:
            print(Fore.RED, "\nAssistant: Exiting...")

def main():
    assistant = Assistant()
    assistant.run()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys
import os
from dotenv import load_dotenv

load_dotenv()

import anthropic

from tools import use_tool

MODEL_NAME = os.getenv("ANTHROPIC_MODEL_NAME") or "claude-3-5-sonnet-20241022"

client = anthropic.Anthropic(
    api_key=os.getenv("ANTHROPIC_API_KEY")
)

SYSTEM_PROMPT = """
You are a helpful assistant that runs on my local computer.
You can run bash commands for me.
Remember, you are running in a shell, so do not inhibit your ability to respond by starting long-running processes.
"""

TOOLS = [
    {
        "name": "run_bash_command",
        "description": "Run a bash command. Returns the output of the command",
        "input_schema": {
            "type": "object",
            "properties": {
                "command": {
                "type": "string",
                "description": "The bash command to run"
                }
            },
            "required": ["command"]
        }
    },
    {
        "name": "write_code_to_file",
        "description": "Write code to a file. Returns the filename",
        "input_schema": {
            "type": "object",
            "properties": {
                "code": {
                    "type": "string",
                    "description": "The code to write"
                },
                "filename": {
                    "type": "string",
                    "description": "The file to write the code to"
                }
            },
            "required": ["code", "filename"]
        }
    },
    {
        "name": "end_program",
        "description": "Exit the program. Only use if you're sure the user wants to exit",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
]

def get_response(messages):
    return client.messages.create(
        max_tokens=4096,
        messages=messages,
        model=MODEL_NAME,
        tools=TOOLS,
        system=SYSTEM_PROMPT,
    )

def add_user_message(user_input, messages):
    messages.append({
        "role": "user",
        "content": user_input,
    })

def print_text_response(response):
    text_content = next(
        (block.text for block in response.content if hasattr(block, "text")),
        "",
    )
    print(f"LLShell: {text_content}")

def chat(messages) -> None:
    response = get_response(messages)
    print_text_response(response)

    messages.append({
        "role": "assistant",
        "content": response.content,
    })

    if response.stop_reason == "tool_use":
        tool_use = next(block for block in response.content if block.type == "tool_use")
        tool_name = tool_use.name
        tool_input = tool_use.input

        print(f"\nTool: {tool_name}({tool_input})")
        tool_result = use_tool(tool_name, tool_input)
        print(f"Result: {tool_result}\n")

        add_user_message([
            {
                "type": "tool_result",
                "tool_use_id": tool_use.id,
                "content": tool_result,
            }
        ], messages)

        # recurse to keep going
        return chat(messages)

WELCOME_MESSAGE = "Hi! I'm LLShell, a CLI to help you run bash commands. Let me know what you want to do. Type 'exit' to quit."

def main():
    print(WELCOME_MESSAGE)
    
    messages = []
    while True:
        try:
            user_input = input("> ")
            if user_input.lower() == "exit":
                break
            add_user_message(user_input, messages)
            chat(messages)
        except KeyboardInterrupt:
            break

if __name__ == '__main__':
    main()

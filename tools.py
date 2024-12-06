import subprocess
import os

def run_bash_command(command):
    try:
        # Ask for user confirmation
        confirmation = input(f"Running command: {command}\nConfirm (y/n)? You can provide a decline reason. ")
        if confirmation.lower() != "y":
            return "User aborted, reason: " + confirmation

        # Run the command
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr}"

def write_code_to_file(code, filename):
    try:
        with open(filename, 'w') as f:
            f.write(code)
        return f"Successfully wrote code to {filename}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

def use_tool(tool_name, tool_input):
    if tool_name == "run_bash_command":
        return run_bash_command(tool_input["command"])
    elif tool_name == "write_code_to_file":
        return write_code_to_file(tool_input["code"], tool_input["filename"])
    else:
        return f"Unknown tool: {tool_name}"
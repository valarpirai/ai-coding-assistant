import os

def read_file(tool_input: dict) -> str:
    """
    Reads the content of a file and returns it as a string.
    
    Args:
        file_path (str): The path to the file to be read.
    
    Returns:
        str: The content of the file.
        
    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there's an error reading the file.
    """
    file_path = tool_input["path"]
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except IOError as e:
        return f"Error reading file '{file_path}': {str(e)}"

def write_file(tool_input: dict) -> str:
    """
    Writes content to a file.
    
    Args:
        file_path (str): The path to the file to be written.
        content (str): The content to write to the file.
    
    Returns:
        str: A message indicating success or failure.
        
    Raises:
        IOError: If there's an error writing to the file.
    """
    file_path = tool_input["path"]
    content = tool_input["content"]
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        return f"Successfully wrote to '{file_path}'."
    except IOError as e:
        return f"Error writing to file '{file_path}': {str(e)}"

def list_files(tool_input: dict) -> str:
    """
    Lists all files in the specified directory.
    
    Args:
        directory (str): The path to the directory to list files from. Defaults to current directory.
    
    Returns:
        str: A string containing the list of files.
        
    Raises:
        FileNotFoundError: If the specified directory does not exist.
    """
    path = tool_input["path"]
    try:
        files = os.listdir(path)
        if not files:
            return f"No files found in '{path}'."
        return "\n".join(files)
    except FileNotFoundError:
        return f"Error: Directory '{path}' not found."
    except PermissionError:
        return f"Error: Permission denied accessing '{path}'."

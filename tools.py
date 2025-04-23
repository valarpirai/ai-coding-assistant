
def read_file(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read()

def write_file(file_path: str, content: str):
    with open(file_path, "w") as file:
        file.write(content)

def list_files(directory: str) -> list[str]:
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]


import os
from llama_index.core import SimpleDirectoryReader

def load_documents(file_name):
    file_path = os.path.join("data", file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ File '{file_name}' not found.")
    return SimpleDirectoryReader(input_files=[file_path]).load_data()

from dotenv import load_dotenv
import os

load_dotenv()

file_search_tool = {
    "type": "file_search",
    "vector_store_ids": [os.getenv("VECTOR_STORE_ID")], # May be an array
}

tools = [file_search_tool] # For each tool
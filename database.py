import json
from typing import List
from models import Todo

DATA_FILE = "todos.json"

todo_list: List[Todo] = []

current_id = 1


def load_data():
    global todo_list, current_id
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            todo_list = [Todo(**item) for item in data]
            if todo_list:
                current_id = max(todo.id for todo in todo_list) + 1
    except (FileNotFoundError, json.JSONDecodeError):
        todo_list = []
        current_id = 1


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump([todo.dict() for todo in todo_list], f, indent=4)

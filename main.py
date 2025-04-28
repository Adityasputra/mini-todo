from fastapi import FastAPI, HTTPException, status
from models import Todo
from database import todo_list
from typing import List

app = FastAPI()

# Get all todos
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todo_list

# Get a specific todo by ID
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    if todo_id < 0 or todo_id >= len(todo_list):
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo_list[todo_id]

# Create a new todo
@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo):
    todo_list.append(todo)
    return {"message": "Todo created successfully", "todo": todo}

# Update an existing todo
@app.put('/todos/{todo_id}', status_code=status.HTTP_200_OK)
def update_todo(todo_id: int, todo: Todo):
    if todo_id < 0 or todo_id >= len(todo_list):
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_list[todo_id] = todo
    return {"message": "Todo updated successfully", "todo": todo}

# Delete a todo
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    if todo_id < 0 or todo_id >= len(todo_list):
        raise HTTPException(status_code=404, detail="Todo not found")
    todo_list.pop(todo_id)
    return {"message": "Todo deleted successfully"}
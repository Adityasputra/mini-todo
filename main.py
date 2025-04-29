from fastapi import FastAPI, HTTPException
from typing import List
from models import Todo, TodoCreate
import database

app = FastAPI()

database.load_data()


@app.get("/todos", response_model=List[Todo])
def get_todos():
    return database.todo_list


@app.get("/todos/filter", response_model=List[Todo])
def filter_todos(completed: bool):
    filtered = [todo for todo in database.todo_list if todo.completed == completed]
    return filtered


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    for todo in database.todo_list:
        if todo.id == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.post("/todos")
def create_todo(todo: TodoCreate):
    new_todo = Todo(
        id=database.current_id,
        title=todo.title,
        description=todo.description,
        completed=todo.completed,
    )
    database.todo_list.append(new_todo)
    database.current_id += 1
    database.save_data()
    return {"message": "Todo created successfully"}


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: TodoCreate):
    for index, todo in enumerate(database.todo_list):
        if todo.id == todo_id:
            database.todo_list[index] = Todo(
                id=todo_id,
                title=updated_todo.title,
                description=updated_todo.description,
                completed=updated_todo.completed,
            )
            database.save_data()
            return {"message": "Todo updated successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for index, todo in enumerate(database.todo_list):
        if todo.id == todo_id:
            database.todo_list.pop(index)
            database.save_data()
            return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

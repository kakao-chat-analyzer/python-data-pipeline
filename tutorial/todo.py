from fastapi import APIRouter, Path, HTTPException, status
from model import Todo, TodoItem, TodoItems
todo_router = APIRouter()

todo_list = []

@todo_router.post('/todo', status_code = 201)
async def add_todo(todo: Todo) -> dict:
    todo_list.append(todo)
    return {
        "message": "Todo added successfully."
    }
@todo_router.get('/todo', response_model = TodoItems)
async def retrieve_todo() -> dict:
    return {
        "todos": todo_list
    }    
    
@todo_router.get("/todo/{todo_id}")
async def get_single_todo(todo_id: int = Path(..., title="The Id of the todo to retrive.")) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {
                "todo": todo
            }
    raise HTTPException(
        status_code = status.HTTP_404_NOT_FOUND,
        detail = "Todo with supplied Id doesn't exist"
    )
    
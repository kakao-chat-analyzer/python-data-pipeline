from fastapi import FastAPI
from todo import todo_router

app = FastAPI()
## cors
# from fastapi.middleware.cors import CORSMiddleware
# origins = ["*"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins = origins,
#     allow_creentials = True,
#     allow_methods = ["*"],
#     allow_headears= ["*"]
# )
@app.get("/")
async def welcome() -> dict:
    return {
        "message": "Hello World"
    }
    
app.include_router(todo_router)

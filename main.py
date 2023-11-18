from fastapi import FastAPI
import uvicorn
from routers import pipeline

app = FastAPI()
app.include_router(pipeline.pipelines, prefix = '/api')

if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1",port=8000,
                reload = True)
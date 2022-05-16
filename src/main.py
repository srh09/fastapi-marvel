import uvicorn
from fastapi import FastAPI
from src.api.handlers import test

app = FastAPI()

app.include_router(test.router, prefix='/api/v1/test')

if __name__ == '__main__':
    uvicorn.run('src.main:app', reload=True)

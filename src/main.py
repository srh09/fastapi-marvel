import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.handlers import character, test

app = FastAPI(
    root_path='/src'
)

app.include_router(test.router)
app.include_router(character.router)
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

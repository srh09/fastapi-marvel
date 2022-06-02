import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.handlers import character, test
from db import base  # noqa: F401 Models must be loaded on app init otherwise SQLAlchemy relationship issues.

app = FastAPI(
    root_path='/src'
)


@app.on_event("startup")
async def startup_event():
    print('things to do when we start-----')
app.include_router(test.router)
app.include_router(character.router)
app.mount("/", StaticFiles(directory="src/static", html=True), name="static")


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

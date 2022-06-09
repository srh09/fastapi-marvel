import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from api.handlers import character, test
from api.handlers import comic
from db import base  # noqa: F401 Models must be loaded on app init otherwise SQLAlchemy relationship issues.

app = FastAPI(
    root_path='/src'
)

origins = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    print('things to do when we start-----')

app.include_router(test.router)
app.include_router(character.router)
app.include_router(comic.router)

app.mount("/", StaticFiles(directory="src/static", html=True), name="static")


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

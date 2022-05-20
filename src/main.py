import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api.handlers import test

app = FastAPI(
    root_path='/src'
)

app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
app.include_router(test.router, prefix='/api/v1/test/t2')


@app.get("/app")
def read_main(request):
    return {"message": "Hello World", "root_path": request.scope.get("root_path")}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)

from fastapi import FastAPI


#instantiating FastAPI class
app = FastAPI()

@app.get("/") #decorators (@) wrap a function and modify its behavior
def read_root():
    return {"message": "Welcome to the FastAPI application!"}

from fastapi import FastAPI
from pydantic import BaseModel
import socket
import os
import uvicorn
import time

app = FastAPI()

class NumbersSchema(BaseModel):
    a: int
    b: int

@app.post("/cal-add")
def add(num: NumbersSchema):
    return {f"sum of {num.a} & {num.b}": num.a + num.b}

@app.get("/cal-sub")
def subtract_numbers(a: int, b: int):
    return {"message": "success", "result": a - b}

@app.get("/cal-mul/{a}/{b}")
def multiply(a: int, b: int):
    return {"message": "success", "result": a * b}

@app.post("/cal-div")
def divide(num: NumbersSchema):
    if num.b == 0:
        return {"message": "error", "result": "Division by zero not allowed"}
    return {"message": "success", "result": num.a / num.b}

def free_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0

def main():
    port = 8000
    if not free_port(port):
        print(f"Port {port} is in use. Killing the process...")
        os.system(f"kill -9 $(lsof -t -i:{port})")
        time.sleep(2)

    uvicorn.run("01_calculator:app", host="127.0.0.1", port=port, reload=True)

if __name__ == "__main__":
    main()

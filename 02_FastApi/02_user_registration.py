from fastapi import FastAPI
from pydantic import BaseModel , EmailStr,Field
import socket
import os
import uvicorn
import time


app = FastAPI()

class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8) 
    id: int


user_json = []

@app.post("/user-registration/")
def user_registration(user: UserSchema):
       
    for existing_user in user_json:
        if existing_user["id"] == user.id:
            return {"message": f"User with ID {user.id} already exists"}
    
    user_json.append(user.model_dump()  )
    return {"message": "User registered successfully", "user_data": user.dict()}

@app.post("/get-all-users/")
def user_registration():
    return user_json

def free_port(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) != 0


def main():
    port = 8000
    if not free_port(port):
        print(f"Port {port} is in use. Killing the process...")
        os.system(f"kill -9 $(lsof -t -i:{port})")
        time.sleep(1)

    uvicorn.run("02_user_registration:app", host="127.0.0.1", port=port, reload=True)

if __name__ == "__main__":
    main()

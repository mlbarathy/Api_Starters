from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def display():
    return "Hello, FastAPI!"


@app.get("/barathy")
def display():
    return "Hi , Barathy.. !"


friends = {1:"mohan",2:"barathy",3:"sundar"}

@app.get("/get-friends/")
def get_friends():
    return friends

@app.get("/get-friend-by-id/{friend_id}")
def get_friend_by_id(friend_id: int):
    return {"id" : friend_id , "friend_name": friends.get(friend_id, "Friend not found")}

@app.get("/add-friend/{id}/{name}")
def add_friend(id: int, name: str):
    friends[id] = name
    return {"message": "Friend added successfully", "friends": friends}

@app.post("/get-all-friends/")
def get_all_friends():
    return friends

from pydantic import BaseModel,StrictInt

class friendModel(BaseModel):
    id: StrictInt
    name: str

@app.post("/post-add-student")
def post_add_student(value: friendModel):
    friends[value.id] = value.name
    return {"message": "Student added successfully" ,
            "friends_list": friends}
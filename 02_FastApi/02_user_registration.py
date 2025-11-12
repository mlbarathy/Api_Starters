from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field
import uvicorn

app = FastAPI(title="In-Memory User Registration API")

# -------------------------------
# Pydantic v2 Model with validation
# -------------------------------
class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr                 # valid email
    password: str = Field(..., min_length=8)  # min 8 chars

# -------------------------------
# In-memory storage
# -------------------------------
user_json = []

# -------------------------------
# Endpoints
# -------------------------------
@app.post("/user-registration/")
def user_registration(user: UserSchema):
    # Prevent duplicate IDs
    for existing_user in user_json:
        if existing_user["id"] == user.id:
            return {"message": f"User with ID {user.id} already exists"}

    user_data = user.model_dump()  # Pydantic v2
    user_json.append(user_data)
    return {"message": "User registered successfully", "user_data": user_data}


@app.get("/get-all-users/")
def get_all_users():
    return {"total_users": len(user_json), "users": user_json}

# -------------------------------
# Main entry
# -------------------------------
if __name__ == "__main__":
    # Simply start Uvicorn server
    uvicorn.run(
        "02_user_registration:app",  # module_name:app_instance
        host="127.0.0.1",
        port=8000,
        reload=True  # hot reload for development
    )

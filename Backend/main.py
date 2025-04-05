from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific domain like ["http://localhost:5500"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# User schema
class User(BaseModel):
    fullname: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# MySQL Connection config
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",       # Your MySQL host
        user="root",            # Your MySQL username
        password="12345",            # Your MySQL password
        database="restaurant"   # Your DB name
    )

@app.post("/signup")
def signup(user: User):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (user.email,))
        if cursor.fetchone():
            raise HTTPException(status_code=400, detail="Email already registered")

        # Insert new user
        cursor.execute(
            "INSERT INTO users (fullname, email, password) VALUES (%s, %s, %s)",
            (user.fullname, user.email, user.password)
        )
        conn.commit()
        conn.close()

        return {"message": "User registered successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/login")
def login(user: LoginRequest):
    try:
        conn = mysql.connector.connect(
            host="localhost", user="root", password="12345", database="restaurant"
        )
        cursor = conn.cursor()

        # Verify user credentials
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (user.email, user.password))
        result = cursor.fetchone()
        conn.close()

        if result:
            return {"message": "Login successful"}
        else:
            raise HTTPException(status_code=401, detail="Invalid email or password")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

app.mount("/static", StaticFiles(directory="Fronted/Code"), name="static")

@app.get("/")
def read_root():
    return FileResponse("Fronted/Code/index.html")
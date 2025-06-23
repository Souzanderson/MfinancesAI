from pydantic import BaseModel, Field
import mysql.connector
from settings import DATABASE_CONFIG
from hashlib import sha1

class User(BaseModel):
    id: int | None = Field(default=None, alias="id")
    username: str = Field(..., alias="username")
    password: str = Field(..., alias="password")  # Store hashed passwords

    @staticmethod
    def hash_password(login:str, password: str) -> str:
        """Hashes a password using SHA-1."""
        return sha1(f"{login}{password}".encode()).hexdigest()

    @staticmethod
    def login(username: str, password: str, db_config: dict = DATABASE_CONFIG):
        """Authenticates a user by username and password."""
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)
        hashkey = User.hash_password(username, password)
        query = """
            SELECT id, username, hashkey
            FROM users
            WHERE hashkey = %s
        """
        cursor.execute(query, (hashkey,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and user["hashkey"]:
            return {"hashkey": user["hashkey"], "id": user["id"], "username": user["username"]}
        else:
            return {"error": "Invalid username or password"}
from pydantic import BaseModel, EmailStr, StringConstraints


class File():
    owner_id: int
    filename: str
    
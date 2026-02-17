from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    endpoint: str
    active: bool = True
    description: str
from pydantic import BaseModel


class EndpointCreate(BaseModel):
    path: str
    method: str
    json_data: str
    group_name: str
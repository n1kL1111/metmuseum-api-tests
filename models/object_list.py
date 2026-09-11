from pydantic import BaseModel, ConfigDict


class ObjectList(BaseModel):
    model_config = ConfigDict(extra="ignore")

    total: int
    objectIDs: list[int]
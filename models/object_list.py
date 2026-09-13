from pydantic import BaseModel, ConfigDict, Field


class ObjectList(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    total: int
    object_ids: list[int]= Field(alias="objectIDs")

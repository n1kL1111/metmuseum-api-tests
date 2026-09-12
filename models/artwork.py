from pydantic import BaseModel, ConfigDict


class Artwork(BaseModel):
    model_config = ConfigDict(extra="ignore")

    objectID: int
    title: str
    department: str
    objectName: str

    artistDisplayName: str
    artistDisplayBio: str

    objectDate: str
    objectBeginDate: int
    objectEndDate: int

    medium: str
    dimensions: str

    isHighlight: bool
    isPublicDomain: bool

    primaryImage: str
    objectURL: str

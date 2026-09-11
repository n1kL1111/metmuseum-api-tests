from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl

from .constituent import Constituent
from .measurement import Measurement
from .tag import Tag


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

    primaryImage: Optional[HttpUrl] = None
    objectURL: Optional[HttpUrl] = None

    constituents: list[Constituent] = []
    measurements: list[Measurement] = []
    tags: list[Tag] = []


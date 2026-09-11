from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class Constituent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    constituentID: int
    role: str
    name: str
    constituentULAN_URL: Optional[HttpUrl] = None
    constituentWikidata_URL: Optional[HttpUrl] = None
    gender: Optional[str] = None

from typing import Optional

from pydantic import BaseModel, ConfigDict, HttpUrl


class Tag(BaseModel):
    model_config = ConfigDict(extra="ignore")

    term: str
    AAT_URL: Optional[HttpUrl] = None
    Wikidata_URL: Optional[HttpUrl] = None
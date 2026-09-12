from pydantic import BaseModel, ConfigDict, HttpUrl


class Constituent(BaseModel):
    model_config = ConfigDict(extra="ignore")

    constituentID: int
    role: str
    name: str
    constituentULAN_URL: str
    constituentWikidata_URL: str
    gender: str


from typing import Optional

from pydantic import BaseModel, ConfigDict


class Measurement(BaseModel):
    model_config = ConfigDict(extra="ignore")

    elementName: str
    elementDescription: Optional[str] = None
    elementMeasurements: dict[str, float]


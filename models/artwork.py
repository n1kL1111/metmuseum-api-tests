from pydantic import BaseModel, ConfigDict, Field



class Artwork(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    object_id: int = Field(alias="objectID")

    title: str
    department: str
    object_name: str = Field(alias="objectName")

    culture: str
    period: str
    dynasty: str
    reign: str
    portfolio: str

    artist_role: str = Field(alias="artistRole")
    artist_display_name: str = Field(alias="artistDisplayName")
    artist_display_bio: str = Field(alias="artistDisplayBio")
    artist_nationality: str = Field(alias="artistNationality")

    object_date: str = Field(alias="objectDate")
    object_begin_date: int = Field(alias="objectBeginDate")
    object_end_date: int = Field(alias="objectEndDate")

    medium: str
    dimensions: str
    classification: str

    is_highlight: bool = Field(alias="isHighlight")
    is_public_domain: bool = Field(alias="isPublicDomain")

    primary_image: str = Field(alias="primaryImage")
    object_url: str = Field(alias="objectURL")
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Constituent(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    constituent_id: int = Field(alias="constituentID")
    role: str = ""
    name: str = ""
    constituent_ulan_url: str = Field("", alias="constituentULAN_URL")
    constituent_wikidata_url: str = Field("", alias="constituentWikidata_URL")
    gender: str = ""


class Measurement(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    element_name: str = Field(alias="elementName")
    element_description: str | None = Field(None, alias="elementDescription")
    element_measurements: dict[str, float] = Field(
        default_factory=dict, alias="elementMeasurements"
    )


class Tag(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    term: str
    aat_url: str = Field("", alias="AAT_URL")
    wikidata_url: str = Field("", alias="Wikidata_URL")


class Artwork(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    object_id: int = Field(alias="objectID")
    is_highlight: bool = Field(alias="isHighlight")
    is_public_domain: bool = Field(alias="isPublicDomain")

    title: str = ""
    department: str = ""
    object_name: str = Field("", alias="objectName")

    culture: str = ""
    period: str = ""
    dynasty: str = ""
    reign: str = ""
    portfolio: str = ""

    artist_role: str = Field("", alias="artistRole")
    artist_display_name: str = Field("", alias="artistDisplayName")
    artist_display_bio: str = Field("", alias="artistDisplayBio")
    artist_nationality: str = Field("", alias="artistNationality")
    artist_begin_date: str = Field("", alias="artistBeginDate")
    artist_end_date: str = Field("", alias="artistEndDate")

    object_date: str = Field("", alias="objectDate")
    object_begin_date: int = Field(alias="objectBeginDate")
    object_end_date: int = Field(alias="objectEndDate")

    medium: str = ""
    dimensions: str = ""
    classification: str = ""

    primary_image: str = Field("", alias="primaryImage")
    primary_image_small: str = Field("", alias="primaryImageSmall")
    object_url: str = Field("", alias="objectURL")

    credit_line: str = Field("", alias="creditLine")
    repository: str = ""
    gallery_number: str = Field("", alias="GalleryNumber")

    metadata_date: datetime = Field(alias="metadataDate")

    additional_images: list[str] = Field(default_factory=list, alias="additionalImages")
    constituents: list[Constituent] = Field(default_factory=list)
    measurements: list[Measurement] = Field(default_factory=list)
    tags: list[Tag] = Field(default_factory=list)

    @field_validator(
        "additional_images",
        "constituents",
        "measurements",
        "tags",
        mode="before",
    )
    @classmethod
    def _none_to_empty_list(cls, value):
        return [] if value is None else value
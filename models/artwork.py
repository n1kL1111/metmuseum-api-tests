from pydantic import BaseModel, ConfigDict, Field


class Artwork(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    # --- Гарантированно есть ---
    object_id: int = Field(alias="objectID")
    is_highlight: bool = Field(alias="isHighlight")
    is_public_domain: bool = Field(alias="isPublicDomain")

    # --- Могут быть пустыми строками / null ---
    title: str | None = None
    department: str | None = None
    object_name: str | None = Field(None, alias="objectName")

    culture: str | None = None
    period: str | None = None
    dynasty: str | None = None
    reign: str | None = None
    portfolio: str | None = None

    artist_role: str | None = Field(None, alias="artistRole")
    artist_display_name: str | None = Field(None, alias="artistDisplayName")
    artist_display_bio: str | None = Field(None, alias="artistDisplayBio")
    artist_nationality: str | None = Field(None, alias="artistNationality")

    object_date: str | None = Field(None, alias="objectDate")
    object_begin_date: int | None = Field(None, alias="objectBeginDate")
    object_end_date: int | None = Field(None, alias="objectEndDate")

    medium: str | None = None
    dimensions: str | None = None
    classification: str | None = None

    primary_image: str | None = Field(None, alias="primaryImage")
    primary_image_small: str | None = Field(None, alias="primaryImageSmall")
    additional_images: list[str] | None = Field(None, alias="additionalImages")
    object_url: str | None = Field(None, alias="objectURL")

    metadata_date: str | None = Field(None, alias="metadataDate")
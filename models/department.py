from pydantic import BaseModel, ConfigDict, Field


class Department(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    department_id: int = Field(alias="departmentId")
    display_name: str = Field(alias="displayName")


class DepartmentsList(BaseModel):
    model_config = ConfigDict(
        extra="ignore",
        populate_by_name=True,
    )

    departments: list[Department]

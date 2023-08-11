"""Request and Response model."""
from pydantic import BaseModel, Field, validator
from typing import List


class UniquePredictionRequest(BaseModel):
    """Request body."""

    id: int = Field(title="user id")
    gender: str = Field(title="user gender")
    age: int = Field(title="user age")
    driving_license: int = Field(title="user driving license")
    region_code: float = Field(title="user region code")
    previously_insured: int = Field(title="previously insurance")
    vehicle_age: str = Field(title="user vehicle age")
    vehicle_damage: str = Field(title="vehicle damage")
    annual_premium: float = Field(title="annual budget")
    policy_sales_channel: float = Field(title="Channel")
    vintage: int = Field(title="Vintage")

    @validator("gender")
    def validate_gender(cls, value):
        """Validate gender."""
        if value not in ["Male", "Female"]:
            raise ValueError("Gender must be 'Male' or 'Female'")
        return value

    @validator("driving_license")
    def validate_driving_license(cls, value):
        """Validate driving license."""
        if value not in [0, 1]:
            raise ValueError("Driving license must be 0 or 1")
        return value

    @validator("previously_insured")
    def validate_previously_insured(cls, value):
        """Validate previously insured."""
        if value not in [0, 1]:
            raise ValueError("Previously insured must be 0 or 1")
        return value

    @validator("vehicle_age")
    def validate_vehicle_age(cls, value):
        """Validate vehicle age."""
        if value not in ["> 2 Years", "1-2 Year", "< 1 Year"]:
            raise ValueError(
                """vehicle age must be present in ['> 2 Years', '1-2 Year',"""
                """'< 1 Year']"""
            )
        return value

    @validator("vehicle_damage")
    def validate_vehicle_damage(cls, value):
        """Validate vehicle damage."""
        if value not in ["Yes", "No"]:
            raise ValueError("vehicle damage must be 'Yes' or 'No'")
        return value


class UniquePredictionResponse(BaseModel):
    """Response body."""

    id: int = Field(title="user id")
    gender: str = Field(title="user gender")
    age: int = Field(title="user age")
    driving_license: int = Field(title="user driving license")
    region_code: float = Field(title="user region code")
    previously_insured: int = Field(title="previously insurance")
    vehicle_age: str = Field(title="user vehicle age")
    vehicle_damage: str = Field(title="vehicle damage")
    annual_premium: float = Field(title="annual budget")
    policy_sales_channel: float = Field(title="Channel")
    vintage: int = Field(title="Vintage")
    score: float

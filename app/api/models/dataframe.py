"""Request and Response model."""
from pydantic import BaseModel, Field
from typing import List


class UniquePredictioRequest(BaseModel):
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

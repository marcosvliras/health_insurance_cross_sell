from pydantic import BaseModel, Field
from typing import List


class DataFrame(BaseModel):
    id: List[int] = Field(title="user id")
    gender: List[str] = Field(title="user gender")
    age: List[int] = Field(title="user age")
    driving_license: List[int] = Field(title="user driving license")
    region_code: List[float] = Field(title="user region code")
    previously_insured: List[int] = Field(title="previously insurance")
    vehicle_age: List[str] = Field(title="user vehicle age")
    vehicle_damage: List[int] = Field(title="vehicle damage")
    annual_premium: List[float] = Field(title="annual budget")
    policy_sales_channel: List[float] = Field(title="Channel")
    vintage: List[int] = Field(title="Vintage")

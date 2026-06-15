from pydantic import BaseModel, field_validator


class PredictRequest(BaseModel):
    prices: list[float]
    month: int
    year: int

    @field_validator("prices")
    @classmethod
    def prices_must_have_six_values(cls, v):
        if len(v) < 12:
            raise ValueError("prices must contain at least 12 values (last 12 months)")
        return v

    @field_validator("month")
    @classmethod
    def month_must_be_valid(cls, v):
        if not 1 <= v <= 12:
            raise ValueError("month must be between 1 and 12")
        return v


class PredictResponse(BaseModel):
    predicted_price: float
    currency: str = "UGX"
    unit: str = "per kg"
    commodity: str = "Maize"
    market: str = "Owino, Kampala"

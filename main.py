from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Distance Converter API", version="1.0.0")


class ConversionResponse(BaseModel):
    kilometers: float
    miles: float


@app.get("/convert", response_model=ConversionResponse)
def convert_km_to_miles(km: float):
    """
    Convert kilometers to miles.
    
    Args:
        km: Distance in kilometers
        
    Returns:
        ConversionResponse with both kilometers and miles
    """
    miles = km * 0.333621371
    return ConversionResponse(kilometers=km, miles=round(miles, 4))

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/ready")
def readiness_check():
    return {"status": "ready"}

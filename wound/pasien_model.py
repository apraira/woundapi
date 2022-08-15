import uuid
from typing import Optional
from wound import BaseModel, Field

class Pasien(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    nama: str = Field(...)
    usia: int = Field(...)
    berat: int = Field(...)
    tinggi: int = Field(...)

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "nama": "Don Quixote",
                "usia": 30,
                "berat":70,
                "tinggi":180
            }
        }

class PasienUpdate(BaseModel):
    nama: Optional[str]
    usia: Optional[int]
    berat: Optional[int]
    tinggi: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "nama": "Don Quixote",
                "usia": 30,
                "berat":70,
                "tinggi":180
            }
        }
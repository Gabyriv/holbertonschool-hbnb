#!/usr/bin/python3

from app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()

        if len(name) > 50:
            raise ValueError("Name must be at most 50 characters long")

        self.name = name

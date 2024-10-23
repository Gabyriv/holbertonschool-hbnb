#!/usr/bin/python3

from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not 1 <= rating <= 5:
            raise ValueError("Rating must be between 1 and 5.")

        if not isinstance(place, Place):
            raise TypeError("Place must be validated.")

        if not isinstance(user, User):
            raise TypeError("User must be validated.")


        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

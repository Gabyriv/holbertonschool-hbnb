#!/usr/bin/python3

from datetime import datetime
from app.models.base_model import BaseModel
class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        if len(first_name) > 50 or len(last_name) > 50:
            raise ValueError("First name and last name must be less than 50 characters")

        if '@' not in email:
            raise ValueError("Invalid email format")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.places = []

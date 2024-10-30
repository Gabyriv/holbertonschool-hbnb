#!/usr/bin/python3

from datetime import datetime
from hbnb.app.models.base_model import BaseModel
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
import re

# This variable is used to validate the email format
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

flask_bcrypt = Bcrypt()

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False, password=None):
        super().__init__()
        self.first_name = self._validate_first_name(first_name)
        self.last_name = self._validate_last_name(last_name)
        self.email = self._validate_email(email)
        self.is_admin = is_admin
        self.places = []
        self.password = self.hash_password(password)

    def _validate_email(self, email):
        if not re.fullmatch(regex, email):
            raise ValueError("Invalid email format")
        return email

    def _validate_first_name(self, first_name):
        if len(first_name) > 50:
            raise ValueError("First name must be less than 50 characters")
        if len(first_name) == 0:
            raise ValueError("First name cannot be empty")
        return first_name
    def _validate_last_name(self, last_name):
        if len(last_name) > 50:
            raise ValueError("Last name must be less than 50 characters")
        if len(last_name) == 0:
            raise ValueError("Last name cannot be empty")
        return last_name

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return flask_bcrypt.check_password_hash(self.password, password)

# Part 3: Authentication, Authorization, and Database Integration

In this phase of the HBnB Project, we've enhanced the application by implementing secure user authentication, role-based authorization, and database persistence using SQLAlchemy. This upgrade brings robust security features and reliable data storage to our application.

## New Features

### Authentication & Security
- Password hashing using Flask-Bcrypt
- JWT-based authentication with Flask-JWT-Extended
- Role-based access control (RBAC)
- Secure login endpoint with token generation
- Protected API endpoints

### Database Integration
- SQLAlchemy ORM implementation
- Entity mapping (User, Place, Review, Amenity)
- Relationship management between entities
- SQLite database for development

## Requirements

```pip
flask
flask-restx
flask-bcrypt
flask-jwt-extended
sqlalchemy
flask-sqlalchemy
```

## Installation

1. Clone this repository:
```bash
git clone <repository>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
flask shell
>>> from app import db
>>> db.create_all()
```

## API Endpoints

### Public Endpoints
- `GET /api/v1/places/`: List all places
- `GET /api/v1/places/<place_id>`: Get place details

### Protected Endpoints (Requires Authentication)
- `POST /api/v1/places/`: Create a new place
- `PUT /api/v1/places/<place_id>`: Update place (owner only)
- `POST /api/v1/reviews/`: Create a review
- `PUT /api/v1/reviews/<review_id>`: Update review (author only)
- `DELETE /api/v1/reviews/<review_id>`: Delete review (author only)
- `PUT /api/v1/users/<user_id>`: Update user profile (self only)

### Admin-Only Endpoints
- `POST /api/v1/users/`: Create new users
- `PUT /api/v1/users/<user_id>`: Modify any user's details
- `POST /api/v1/amenities/`: Add new amenities
- `PUT /api/v1/amenities/<amenity_id>`: Modify amenities

## Authentication

To access protected endpoints, include the JWT token in the Authorization header:
```bash
Authorization: Bearer <your_jwt_token>
```

## Authors

- [@Gabyriv](https://www.github.com/gabyriv)

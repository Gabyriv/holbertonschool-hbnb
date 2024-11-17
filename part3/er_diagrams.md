```mermaid
erDiagram
    User {
        CHAR(36) id
        VARCHAR first_name
        VARCHAR last_name
        VARCHAR email
        VARCHAR password
        BOOLEAN is_admin
    }

    Place {
        CHAR(36) id
        VARCHAR title
        VARCHAR description
        DECIMAL price
        FLOAT latitude
        FLOAT longitude
        CHAR(36) owner_id
    }

    Amenity {
        CHAR(36) id
        VARCHAR name
    }

    Review {
        CHAR(36) id
        VARCHAR text
        INT rating
        CHAR(36) place_id
        CHAR(36) user_id
    }

    Place_Amenity {
        CHAR(36) place_id
        CHAR(36) amenity_id
    }

    User ||--o{ Place : "owns"
    User ||--o{ Review: "author"
    Place ||--o{ Place_Amenity : "can have"
    Place ||--o{ Review : "has reviews"
    Amenity ||--o{ Place_Amenity : "are in places"

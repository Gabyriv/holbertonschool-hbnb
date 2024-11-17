-- User Table
CREATE TABLE IF NOT EXISTS User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Place Table
CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User (id)
);

-- Review Table
CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT NOT NULL CHECK (
        rating >= 1
        AND rating <= 5
    ),
    user_id CHAR(36),
    place_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES User (id),
    FOREIGN KEY (place_id) REFERENCES Place (id),
    UNIQUE (user_id, place_id)
);

-- Amenity Table
CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

-- Place_Amenity Table
CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id CHAR(36),
    amenity_id CHAR(36),
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place (id),
    FOREIGN KEY (amenity_id) REFERENCES Amenity (id)
);

-- Initial Data User
INSERT INTO
    User (
        id,
        email,
        first_name,
        last_name,
        password,
        is_admin
    )
VALUES (
        '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
        'admin@hbnb.io',
        'Admin',
        'HBnB',
        '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj2NNJj.8fbu',
        TRUE
    );

-- Initial Data Amenities
INSERT INTO
    Amenity (id, name)
VALUES (
        '550e8400-e29b-41d4-a716-446655440000',
        'Wifi'
    ),
    (
        '550e8400-e29b-41d4-a716-446655440001',
        'Swimming Pool'
    ),
    (
        '550e8400-e29b-41d4-a716-446655440002',
        'Air Conditioning'
    );

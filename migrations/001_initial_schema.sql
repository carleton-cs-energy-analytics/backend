CREATE TABLE buildings (
  building_id SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE rooms (
  room_id     SERIAL PRIMARY KEY,
  name        VARCHAR(32) NOT NULL UNIQUE,
  building_id INT         NOT NULL REFERENCES buildings,
  floor       INT         NOT NULL,
  description TEXT
);

CREATE TABLE devices (
  device_id   SERIAL PRIMARY KEY,
  name        VARCHAR(255),
  room_id     INT NOT NULL REFERENCES rooms,
  description TEXT
);

CREATE TABLE enumerations (
  enumeration_id SERIAL PRIMARY KEY,
  cases          JSONB
);

CREATE TYPE VALUE_TYPE_CATEGORY AS ENUM ('bool', 'int', 'double', 'enum');
-- we're overloading the word "category" a little here.

CREATE TABLE value_type (
  value_type_id  SERIAL PRIMARY KEY,
  category       VALUE_TYPE_CATEGORY NOT NULL,
  enumeration_id INT REFERENCES enumerations
);

CREATE TABLE value_units (
  value_units_id SERIAL PRIMARY KEY,
  measurement    VARCHAR(255) NOT NULL,
  units          VARCHAR(255) NOT NULL
);

CREATE TABLE points (
  point_name     VARCHAR(255) PRIMARY KEY,
  device_id      INT NOT NULL REFERENCES devices,
  value_type_id  INT NOT NULL REFERENCES value_type,
  value_units_id INT REFERENCES value_units,
  description    TEXT
);

CREATE TABLE categories (
  category_id SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE tags (
  tag_id      SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL UNIQUE,
  category_id INT REFERENCES categories,
  description TEXT
);

CREATE TABLE buildings_tags (
  building_id INT NOT NULL REFERENCES buildings,
  tag_id      INT NOT NULL REFERENCES tags
);

CREATE TABLE rooms_tags (
  room_id INT NOT NULL REFERENCES rooms,
  tag_id  INT NOT NULL REFERENCES tags
);

CREATE TABLE devices_tags (
  device_id INT NOT NULL REFERENCES devices,
  tag_id    INT NOT NULL REFERENCES tags
);

CREATE TABLE points_tags (
  point_name VARCHAR(255) NOT NULL REFERENCES points,
  tag_id     INT          NOT NULL REFERENCES tags
);

CREATE TABLE values (
  value_id   SERIAL PRIMARY KEY,
  point_name VARCHAR(255) NOT NULL REFERENCES points,
  timestamp  INT          NOT NULL,
  int        BIGINT,
  double     DOUBLE PRECISION
);

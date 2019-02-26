CREATE TABLE buildings (
  building_id SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL UNIQUE
)
;

CREATE TABLE rooms (
  room_id     SERIAL PRIMARY KEY,
  name        VARCHAR(32) NOT NULL,
  building_id INT         NOT NULL REFERENCES buildings,
  floor       INT,
  description TEXT,
  UNIQUE (name, building_id)
)
;

CREATE TABLE devices (
  device_id   SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  room_id     INT          NOT NULL REFERENCES rooms,
  description TEXT,
  UNIQUE (name, room_id)
)
;

CREATE TABLE value_types (
  value_type_id SERIAL PRIMARY KEY,
  name          VARCHAR(255) NOT NULL UNIQUE,
  type          JSONB        NOT NULL
)
;

CREATE TABLE value_units (
  value_unit_id SERIAL PRIMARY KEY,
  measurement   VARCHAR(255) NOT NULL,
  unit          VARCHAR(255) NOT NULL,
  UNIQUE (measurement, unit)
)
;

CREATE TABLE points (
  point_id      SERIAL PRIMARY KEY,
  name          VARCHAR(255) NOT NULL UNIQUE,
  device_id     INT          NOT NULL REFERENCES devices,
  value_type_id INT REFERENCES value_types,
  value_unit_id INT REFERENCES value_units,
  description   TEXT
)
;

CREATE TABLE categories (
  category_id SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL UNIQUE
)
;

CREATE TABLE tags (
  tag_id      SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL UNIQUE,
  category_id INT REFERENCES categories,
  description TEXT
)
;

CREATE TABLE buildings_tags (
  building_id INT NOT NULL REFERENCES buildings,
  tag_id      INT NOT NULL REFERENCES tags,
  UNIQUE (building_id, tag_id)
)
;

CREATE TABLE rooms_tags (
  room_id INT NOT NULL REFERENCES rooms,
  tag_id  INT NOT NULL REFERENCES tags,
  UNIQUE (room_id, tag_id)
)
;

CREATE TABLE devices_tags (
  device_id INT NOT NULL REFERENCES devices,
  tag_id    INT NOT NULL REFERENCES tags,
  UNIQUE (device_id, tag_id)
)
;

CREATE TABLE points_tags (
  point_id INT NOT NULL REFERENCES points,
  tag_id   INT NOT NULL REFERENCES tags,
  UNIQUE (point_id, tag_id)
)
;

CREATE TABLE values (
  value_id  SERIAL PRIMARY KEY,
  point_id  INT NOT NULL,
  timestamp INT NOT NULL,
  int       BIGINT,
  double    DOUBLE PRECISION,
  CHECK ((int IS NULL AND double IS NOT NULL) OR (int IS NOT NULL AND double IS NULL)),
  UNIQUE (point_id, timestamp)
)
;

CREATE TABLE rules (
  rule_id      SERIAL PRIMARY KEY,
  name         VARCHAR(255) NOT NULL UNIQUE,
  priority     INT          NOT NULL DEFAULT 1,
  url          TEXT         NOT NULL,
  point_search TEXT         NOT NULL,
  value_search TEXT         NOT NULL
)
;

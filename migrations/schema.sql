/*
Links building name to building ID
*/
CREATE TABLE buildings (
  building_id SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL UNIQUE
)
;

/*
How to relate room_id’s to the actual rooms. Also tells us which building and floor each room is in/on.
*/
CREATE TABLE rooms (
  room_id     SERIAL PRIMARY KEY,
  name        VARCHAR(32) NOT NULL,
  building_id INT         NOT NULL REFERENCES buildings, -- Foreign Key
  floor       INT,
  description TEXT,
  UNIQUE (name, building_id)
)
;

/*
Relates device IDs to their name. As of now (Spring 2021), this table is only being used to connect points to which rooms they are in.
  In the future this could be used to pinpoint which exact devices are connected to which points. Devices are not being used now, just points.
*/
CREATE TABLE devices (
  device_id   SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL,
  room_id     INT          NOT NULL REFERENCES rooms, -- Foreign Key
  description TEXT,
  UNIQUE (name, room_id)
)
;

/*
How to relate the value_type_id’s to their names (boolean, OFF_ON, SS PUMP LL, etc.)
  and what values each type can have ([“FALSE”, “TRUE”], [“OFF”, “ON”], [“P1”, “P2”, “P3”], etc.).
*/
CREATE TABLE value_types (
  value_type_id SERIAL PRIMARY KEY,
  name          VARCHAR(255) NOT NULL UNIQUE,
  type          JSONB        NOT NULL
)
;

/*
How to relate value_unit_id’s to what they are measuring and what their units.
  For example, if a point has a value_unit_id = 1, it measures ‘temperature’ in ‘degrees fahrenheit’.
  As of now, (Spring 2021), these are only the units for integer or float value_types - there are not value_units for other value_types.
*/
CREATE TABLE value_units (
  value_unit_id SERIAL PRIMARY KEY,
  measurement   VARCHAR(255) NOT NULL,
  unit          VARCHAR(255) NOT NULL,
  UNIQUE (measurement, unit)
)
;

/*
All of the points in the database and their info. To find what a point is measuring, look up its value_type_id in the value_types table.
  If a point does not have a value_unit_id, then it is not measuring something with a unit
*/
CREATE TABLE points (
  point_id      SERIAL PRIMARY KEY,
  name          VARCHAR(255) NOT NULL UNIQUE,
  device_id     INT          NOT NULL REFERENCES devices, -- Foreign Key
  value_type_id INT REFERENCES value_types,
  value_unit_id INT REFERENCES value_units,
  description   TEXT
)
;

-- This table does nothing as of now
CREATE TABLE categories (
  category_id SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL UNIQUE
)
;

/*
Tags are the types of points, devices, or buildings such as ‘Room Temperature’,  ‘Radiation Valve’ or ‘Academic’.
  This table tells us how to relate the tag_id’s to exact tag names.
*/
CREATE TABLE tags (
  tag_id      SERIAL PRIMARY KEY,
  name        VARCHAR(255) NOT NULL UNIQUE,
  category_id INT REFERENCES categories, -- Foreign Key - always NULL as of Spring 2021
  description TEXT
)
;

/*
Relates building_id to tag_id.
  Tells us if a building is Academic or Residential - More tags can be added as more types of buildings arise
*/
CREATE TABLE buildings_tags (
  building_id INT NOT NULL REFERENCES buildings, -- Foreign Key
  tag_id      INT NOT NULL REFERENCES tags, -- Foreign Key
  UNIQUE (building_id, tag_id)
)
;

/*
Relates room_id to tag_id. Nothing in here as of Spring 2021.
*/
CREATE TABLE rooms_tags (
  room_id INT NOT NULL REFERENCES rooms, -- Foreign Key
  tag_id  INT NOT NULL REFERENCES tags, -- Foreign Key
  UNIQUE (room_id, tag_id)
)
;

/*
Relates device_id to tag_id - not much in here as of Spring 2021
  Note: We are not using devices at this time, but this will be useful when/if a group starts using them
*/
CREATE TABLE devices_tags (
  device_id INT NOT NULL REFERENCES devices, -- Foreign Key
  tag_id    INT NOT NULL REFERENCES tags, -- Foreign Key
  UNIQUE (device_id, tag_id)
)
;

/*
Relates point_id’s to tag_id’s. Tells us the type of each point
*/
CREATE TABLE points_tags (
  point_id INT NOT NULL REFERENCES points, -- Foreign Key
  tag_id   INT NOT NULL REFERENCES tags, -- Foreign Key
  UNIQUE (point_id, tag_id)
)
;

/*
This is a list of all of the values spit out from the devices.
  It tells us which point is related to each value along with the timestamp.
  You then can look at the points table (to get the value_type_id and value_unit_id) to see what the values are measuring.
  Note: This table only has integer and double/float values. The other value types are encoded in integers (Ex. True = 1 and False = 0 for a boolean).
*/
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

/*
The name of the rule, (not sure what priority is) and its ID.
  It also tells us the url that gets added onto the API base URL to search for that rule.
  Point_search tells us how it searches for points (which points it’s looking for) and value_search tells us the values that signal an anomaly.
  We are not using rules anymore in Spring 2021 - focusing on ML anomaly detecton techniques.
*/
CREATE TABLE rules (
  rule_id      SERIAL PRIMARY KEY,
  name         VARCHAR(255) NOT NULL UNIQUE,
  priority     INT          NOT NULL DEFAULT 1,
  url          TEXT         NOT NULL,
  point_search TEXT         NOT NULL,
  value_search TEXT         NOT NULL
)
;

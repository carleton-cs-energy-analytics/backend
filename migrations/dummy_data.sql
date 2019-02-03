INSERT INTO buildings (building_id, name)
VALUES (1, 'CMC')
     , (2, 'Evans')
     , (3, 'Burton')
     , (4, 'Davis')
     , (5, 'Boliou')
     , (6, 'Sayles')
;

INSERT INTO rooms (room_id, name, building_id, floor, description)
VALUES (1, '328', 1, 3, 'Fishbowl')
     , (2, '304', 1, 3, NULL)
     , (3, '102', 1, 1, NULL)
     , (4, '107', 2, 1, NULL)
     , (5, '113', 6, 1, 'Sayles Great Space')
;

INSERT INTO devices (device_id, room_id, name)
VALUES (1, 1, 'Fishbowl thermostat')
     , (2, 1, 'Fishbowl vav')
     , (3, 4, 'Thermostat in Evans 107')
     , (4, 3, '102 Lab thermostat')
;

INSERT INTO points (point_id, name, device_id, value_type_id, value_unit_id, description)
VALUES (1, 'CMC.328.RT', 1, 2, 1, 'Room Temp in CMC 328')
     , (2, 'CMC.328.SP', 1, 4, 1, 'Thermostat Set Point in CMC 328')
     , (3, 'EV.RM107.RT', 3, 2, 1, 'Room Temp in Evans 107')
     , (4, 'EV.RM107.SP', 3, 3, 1, 'Thermostat Set Point in Evans 107')
     , (5, 'CMC.102.SP', 4, 2, 1, 'Thermostat Set Point in CMC 102')
;

INSERT INTO categories (category_id, name)
VALUES (1, 'device_type')
     , (2, 'building_usage_type')
     , (3, 'room_type')
     , (4, 'residence_occupancy_size')
     , (5, 'department')
;

INSERT INTO tags (name, category_id)
VALUES ('thermostat', 1)
     , ('set', NULL)
     , ('get', NULL)
     , ('residential', 2)
     , ('academic', 2)  -- 5
     , ('residence', 3)
     , ('single', 4)
     , ('room_temp', NULL)
     , ('classroom', 3) -- 9
     , ('math_stats', 5)
     , ('computer_science', 5)
;

INSERT INTO points_tags (point_id, tag_id)
VALUES (1, 3)
     , (2, 2)
     , (3, 3)
     , (4, 2)
     , (1, 8)
     , (2, 8)
     , (3, 8)
     , (4, 8)
     , (5, 2)
;

INSERT INTO devices_tags (device_id, tag_id)
VALUES (1, 1)
     , (3, 1)
;

INSERT INTO rooms_tags (room_id, tag_id)
VALUES (1, 9)
     , (4, 6)
     , (4, 7)
;

INSERT INTO buildings_tags (building_id, tag_id)
VALUES (1, 5)
     , (1, 10)
     , (1, 11)
     , (2, 4)
;

INSERT INTO values (point_id, timestamp, int, double)
VALUES (1, 2, 6, NULL)
     , (4, 5, NULL, 9.8)
     , (3, 13, 10, NULL)
     , (2, 35, 1, NULL)
;

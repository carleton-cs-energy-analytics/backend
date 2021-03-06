INSERT INTO value_units (measurement, unit)
VALUES ('temperature', 'fahrenheit')
     , ('temperature', 'celsius')
     , ('airflow', 'feet^3 minute^-1')
;

-- The values below are the first pass at figuring out all the
-- possible enum types. (We're ignoring `TIME` entirely for now.)
INSERT INTO value_types (name, type)
VALUES ('Boolean', 'true')
     , ('Integer', '1')
     , ('Float', '1.0')
     , ('BACNET EVENT ENROLLMENT', '["NRML", "FAULT", "OFFNRML", "HIGH", "LOW"]')
     , ('BACNET LENUM', '["NIGHT", "DAY", "SPECIAL2", "SPECIAL3", "SPECIAL4", "SPECIAL5"]')
     , ('BLEED_HOLD', '["No", "Yes"]')
     , ('CHLR45', '["CH", "CH"]')
     , ('CHLR_SEQ', '["0", "1", "2", "3", "4", "5", "43", "53", "54", "543"]')
     , ('CLEAN_DIRTY', '["CLEAN", "DIRTY"]')
     , ('CLOSED_OPEN', '["CLOSED", "OPEN"]')
     , ('COOL_HEAT', '["COOL", "HEAT"]')
     , ('DISABL_ENABLE', '["DISABL", "ENABLE"]')
     , ('Default L2SL', '["OFF", "ON"]')
     , ('Default L2SP', '["OFF", "ON"]')
     , ('Default LDI', '["OFF", "ON"]')
     , ('Default LDO', '["OFF", "ON"]')
     , ('EQS_OFF_ON', '["OFF", "ON"]')
     , ('ETS_STE', '["ETS", "STE"]')
     , ('Generic_-5001', '["INACTIVE", "DRIVE"]')
     , ('Generic_-5002', '["HEAT", "DRY", "COOL", "FAN", "AUTO"]')
     , ('Generic_-5003', '["AUTO", "QUIET", "WEAK", "STRONG", "5"]')
     , ('Generic_-5004', '["AUTO", "2", "3", "4", "5", "6", "SWING"]')
     , ('Generic_-5005', '["DEG", "DEG"]')
     , ('Generic_-5007', '["AUTO", "HAND"]')
     , ('Generic_-5008', '["OK", "ALARM"]')
     , ('Generic_-5010', '["INACTIVE", "READY"]')
     , ('Generic_-5011', '["DISABLE", "ENABLE"]')
     , ('Generic_-5014', '["NO", "FLOW"]')
     , ('Generic_2000', '["Off", "On"]')
     , ('Generic_2001', '["No", "Yes"]')
     , ('Generic_2002', '["Stopped", "Running"]')
     , ('HOLD_FILL', '["HOLD", "FILL"]')
     , ('LOAD_SHED', '["NONE", "STAGE", "STAGE", "STAGE"]')
     , ('LOCAL_REMOTE', '["LOCAL", "REMOTE"]')
     , ('LO_HI', '["LO", "HI"]')
     , ('NEG_POS', '["NEG", "POS"]')
     , ('NIGHT_DAY', '["NIGHT", "DAY"]')
     , ('NORMAL_ALARM', '["NORMAL", "ALARM"]')
     , ('NORMAL_FAIL', '["NORMAL", "FAIL"]')
     , ('NORMAL_LOCKOUT', '["NORMAL", "LOCKOUT"]')
     , ('NO_RESET', '["NO", "RESET"]')
     , ('NO_YES', '["NO", "YES"]')
     , ('NTRAL_ACTIVE', '["NTRAL", "ACTIVE"]')
     , ('OFF_ON', '["OFF", "ON"]')
     , ('OK_FAULT', '["OK", "FAULT"]')
     , ('ONE_TWO', '["ONE", "TWO"]')
     , ('OPERATION_PHASE',
        '["OFF", "HTDURVAC", "CLDURVAC", "STRT_HTG", "REGULATG", "STOP_HTG", "STOP_CLG", "POST_HTG", "POST_CLG"]')
     , ('REC_HX_PUMP_LEAD', '["P2", "P1"]')
     , ('RESET_HERE', '["RESET", "ALARM"]')
     , ('SS PUMP LL', '["P1", "P2", "P3"]')
     , ('SSTO_OPERATION', '["NONE", "HEATING", "COOLING", "BOTH"]')
     , ('START_MODE', '["STRT_HTG", "STRT_CLG", "NO_STRT"]')
     , ('STOP_MODE', '["STOP_HTG", "STOP_CLG", "STOP_HOC", "NO_STOP"]')
     , ('STOP_RUN', '["STOP", "RUN"]')
     , ('STOP_START', '["STOP", "START"]')
     , ('UNOCC_OCC', '["UNOCC", "OCC"]')
     , ('VFD SAFETY', '["NORMAL", "LOCKOUT"]')
     , ('ZONE_MODE',
        '["VAC", "OCC1", "OCC2", "OCC3", "OCC4", "OCC5", "WARMUP", "COLLDOWN", "NGHT_HTG", "STOP_HTG", "STOP_CLG"]')
     , ('boolean', '["FALSE", "TRUE"]')
;


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

INSERT INTO value_units (measurement, unit)
VALUES ('temperature', 'degrees fahrenheit')
     , ('proportion open', 'percent')
     , ('volume', 'gallons')
     , ('proportion closed', 'percent')
     , ('humidity', 'percent')
     , ('energy', 'kilowatt hours')
     , ('mass', 'pounds')
     , ('pounds per unit time', 'pounds per hour')
     , ('frequency', 'hertz')
     , ('volume per unit time', 'gallons per minute')
     , ('pressure', 'pounds per square inch')
     , ('pressure differential', 'pounds per square inch')
     , ('volume per unit time', 'cubic feet per minute')
     , ('area', 'square feet')
     , ('power', 'horsepower')
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
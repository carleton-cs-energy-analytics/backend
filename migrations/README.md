# Energy Comps Database
Welcome to the ENergy Comps Database! To view the database schema and documentation on each table, see *schema.sql*. To learn more about how to query the database, see below.

# Useful Database Queries
This document gives some useful examples of queries to the Energy Database. This is a great place to start if first looking at the database or you're trying to get lots of information and would like an initial idea for how to structure your search query.

Each task has a query and one or more variables that you must change to specify your search. Some give the format of the tuples the query returns, since it is not obvious. A few also have steps/multiple queries you should follow to complete your desired task.

Feel free to add to this document as your find more useful database queries that are commonly used.

## Finding Information on Objects
### Find point with a certain id:
**Query:** SELECT * FROM points WHERE point_id = **<point_id>**;\
**<point_id>** = the point_id of the point you would like to search for

### Find all points in a certain room:
**Query:** SELECT * FROM points WHERE device_id IN (SELECT device_id FROM devices WHERE room_id = **<room_id>**);\
**<room_id>** = the room_id of the room you would like to find points for

### Find all points in a certain building:
**Query:** SELECT * FROM points WHERE device_id IN (SELECT device_id FROM devices WHERE room_id IN (SELECT room_id FROM rooms WHERE building_id = **<building_id>**));\
**<building_id>** = the building_id of the room you would like to find points for

### Find all points that have names containing a certain substring:
**Query:** SELECT * FROM points WHERE name LIKE ‘%**<substring>**%’;\
**<substring>** = the substring you would like to search for

### Find all points with a certain tag:
**Query:** SELECT * FROM points WHERE point_id in (SELECT point_id FROM points_tags WHERE tag_id = **<tag_id>**);\
**<tag_id>** = the tag_id of the tag you would like to search for

### Get all relevant info for points from a certain building:
**Returns tuples in format:** (point_name, point_id, tag_id, room_id, room_name, floor, building_id)\
**Query:** SELECT P.name, P.point_id, T.tag_id, R.room_id, R.name, R.floor, R.building_id FROM ((points as P JOIN points_tags as T ON P.point_id = T.point_id) JOIN devices AS D ON P.device_id=D.device_id) JOIN rooms as R ON R.room_id = D.room_id WHERE building_id = **<building_id>**;\
**<building_id>** = building_id of the building you would like to query\
**Potential Modifications:**
- Change the WHERE clause to filter the data in a different way (ex. WHERE point_id = 1 to get all info for point 1)
- Can also select different attributes from the tables if you do not want all of that information

## Altering the Database
### If there is a duplicate tag in the database that you would like to delete, follow this process:
1. Delete duplicate points:
	1. UPDATE points_tags SET tag_id = **<new_id>** WHERE tag_id = **<old_id>**;
		- **<new_id>** = tag_id you would like to keep
		- **<old_id>** = tag_id you would like to remove
	2. Remove old points:
		1. DELETE FROM tags WHERE tag_id = **<old_id>**;
			- **<old_id>** = tag_id you would like to remove

### If you want to set a certain set of points to a certain tag:
**Query:** UPDATE points_tags SET tag_id = **<new_id>** WHERE point_id IN (**<point_ids>**);\
**<new_id>** = tag_id you would like to set this group of points to\
**<point_ids>** = The set of point_id’s of points you would like to change the tag_id of\
	Note: you should ‘SELECT point_id’ in your **<point_ids>** but SELECT nothing else

## Useful for Pulling Data For ML Techniues
### Get all rooms in a building with three certain point types:
**Returns tuples format:** (room_name, point_id_1, point_id_2, point_id_3)\
**Query:** WITH DR as (SELECT D.device_id, R.name from rooms as R JOIN devices as D ON D.room_id = R.room_id WHERE R.building_id = **<building_id>** AND R.name NOT LIKE 'UnID%')\
SELECT P3.room, pid1, pid2, pid3 FROM (SELECT P1.point_id as pid1, P2.point_id as pid2, P2.name as room FROM (SELECT P.point_id, DR.name FROM points as P JOIN DR ON DR.device_id = P.device_id WHERE P.point_id IN (SELECT point_id FROM points_tags WHERE tag_id = **<tag_id_1>**)) as P1 JOIN (SELECT P.point_id, DR.name FROM points as P JOIN DR ON DR.device_id = P.device_id WHERE P.point_id IN (SELECT point_id FROM points_tags WHERE tag_id = **<tag_id_2>**)) as P2 ON P1.name=p2.name) as P4 JOIN (SELECT P.point_id as pid3, DR.name as room FROM points as P JOIN DR ON DR.device_id = P.device_id WHERE P.point_id IN (SELECT point_id FROM points_tags WHERE tag_id = **<tag_id_3>**)) as P3 ON P3.room=P4.room ORDER BY P3.room;\
**<building_id>** = the id of the building you would like to look in\
**<tag_id_1>** = the tag_id of the first type of point you want to find\
**<tag_id_2>** = the tag_id of the second type of point you want to find\
**<tag_id_3>** = the tag_id of the third type of point you want to find

### Get all rooms in a building with two certain point types:
**Returns tuples format:** (room_name, point_id_1, point_id_2)\
**Query:** WITH DR as (SELECT D.device_id, R.name from rooms as R JOIN devices as D ON D.room_id = R.room_id WHERE R.building_id = **<building_id>** AND R.name NOT LIKE 'UnID%')\
SELECT P2.name as room, P1.point_id as pid1, P2.point_id as pid2 FROM (SELECT P.point_id, DR.name FROM points as P JOIN DR ON DR.device_id = P.device_id WHERE P.point_id IN (SELECT point_id FROM points_tags WHERE tag_id = **<tag_id_1>**)) as P1 JOIN (SELECT P.point_id, DR.name FROM points as P JOIN DR ON DR.device_id = P.device_id WHERE P.point_id IN (SELECT point_id FROM points_tags WHERE tag_id = **<tag_id_2>**)) as P2 ON P1.name=p2.name ORDER BY room;\
**<building_id>** = the id of the building you would like to look in\
**<tag_id_1>** = the tag_id of the first type of point you want to find
**<tag_id_2>** = the tag_id of the second type of point you want to find

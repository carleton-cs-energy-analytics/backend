.PHONY: run schema seed

run:
	DATABASE_HOST=localhost DATABASE_NAME=energy DATABASE_USER=energy DATABASE_PASSWORD="[REDACTED]" pipenv run gunicorn --bind energycomps.its.carleton.edu:8080 --log-file /home/energy/logs/gunicorn.log run &

debug:
	FLASK_DEBUG=1 DATABASE_HOST=localhost DATABASE_NAME=energy DATABASE_USER=energy DATABASE_PASSWORD="[REDACTED]" pipenv run gunicorn --bind energycomps.its.carleton.edu:8080 --log-file /home/energy/logs/gunicorn.log run &

schema:
	PGPASSWORD="[REDACTED]" /usr/pgsql-10/bin/psql -h localhost -d energy -U energy -f ./migrations/001_initial_schema.sql

seed:
	PGPASSWORD="[REDACTED]" /usr/pgsql-10/bin/psql -h localhost -d energy -U energy -f ./migrations/seed.sql


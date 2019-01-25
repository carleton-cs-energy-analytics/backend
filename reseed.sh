#!/usr/bin/env bash

dropdb energy-dev; \
createdb energy-dev && \
psql energy-dev -f ./migrations/schema.sql && \
psql energy-dev -f ./migrations/seed.sql

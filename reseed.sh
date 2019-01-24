#!/usr/bin/env bash

dropdb energy-dev; \
createdb energy-dev && \
psql energy-dev -f ./migrations/001_initial_schema.sql && \
psql energy-dev -f ./migrations/real_seed.sql

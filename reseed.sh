#!/usr/bin/env bash

psql energy-dev -f ./migrations/down.sql && \
psql energy-dev -f ./migrations/schema.sql && \
psql energy-dev -f ./migrations/seed.sql

#!/usr/bin/env bash

psql energy-test -f ./migrations/drop.sql && \
psql energy-test -f ./migrations/schema.sql && \
psql energy-test -f ./migrations/seed.sql && \
psql energy-test -f ./migrations/dummy_data.sql

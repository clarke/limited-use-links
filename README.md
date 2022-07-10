# Limited Use Links

## Purpose

This application allows for sharing a unique URL a single time, after which it expires and is no longer available.

## Setup

To do the inital setup, run:

`$ make install_requirements`

`$ make init_db`

## Scripts

To add a new user to the database, run:

`$ python3 ./scripts/add_user.py`

This assumes that the database and schema have all been created.

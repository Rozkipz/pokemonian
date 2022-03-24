image_name := env_var_or_default("IMAGE_NAME", "pokeapi")

# Needed if the pyproject toml is updated. This updates the lock file.
update_reqs:
	poetry update

# Run the crawler and API
run *args:
	DB_CONN="postgresql://postgres:postgres@db:5432/postgres" docker-compose up {{args}}

# Run the crawler with DEBUG enabled.
debug *args:
	DEBUG=True just run

# Force build the docker compose containers.
force_run:
	just run --force-recreate --build --no-deps

# Build the pokemon api image.
docker_build:
	docker build . -t {{image_name}}:latest

# Remove the postgres db
_remove_postgres_db:
	docker-compose down --volumes

# Run the tests
test: docker_build
	#!/usr/bin/env bash
	set -euxo pipefail

	# Remove existing DB
	just _remove_postgres_db

	# Create a new postgres DB
	docker-compose up -d db

	# Let the DB start up
	sleep 2

	# Create the DB table
	docker run -e DB_CONN="postgresql://postgres:postgres@host.docker.internal:5432/postgres" --add-host=host.docker.internal:host-gateway {{image_name}}:latest "poetry run alembic upgrade head"

	# Run the tests
	docker run --add-host=host.docker.internal:host-gateway {{image_name}}:latest "poetry run pytest"

	# Shutdown the postgres DB.
	docker-compose down
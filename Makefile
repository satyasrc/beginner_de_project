####################################################################################################################
# Setup containers to run Airflow

docker-spin-up:
	docker compose build --no-cache && docker compose up airflow-init && docker compose up --build -d

perms:
	sudo mkdir -p logs plugins temp dags tests data visualization && sudo chmod -R u=rwx,g=rwx,o=rwx logs plugins temp dags tests data visualization

debug:
	-docker exec -u airflow scheduler ls -la /home/airflow/.local/bin/airflow

setup-conn:
	docker cp containers/airflow/setup_conn.py scheduler:/opt/airflow/setup_conn.py
	docker exec -u airflow scheduler python /opt/airflow/setup_conn.py

do-sleep:
	sleep 30

up: perms docker-spin-up do-sleep

down:
	docker compose down

restart: down up

sh:
	docker exec -ti webserver bash

####################################################################################################################
# Testing, auto formatting, type checks, & Lint checks
pytest:
	docker exec webserver pytest -p no:warnings -v /opt/airflow/tests

format:
	docker exec webserver python -m black -S --line-length 79 .

isort:
	docker exec webserver isort .

type:
	docker exec webserver mypy --ignore-missing-imports /opt/airflow

lint: 
	docker exec webserver flake8 /opt/airflow/dags

ci: isort format type lint pytest


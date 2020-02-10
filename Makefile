RUN=docker-compose run --rm project

all:
	docker-compose build

run:
	docker-compose up project

shell:
	docker-compose run --rm project /bin/bash

test:
	$(RUN) pytest -x -vvv --pdb

stop:
	docker-compose down
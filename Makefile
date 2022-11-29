include .env
service := data_ingestion

build:
	docker-compose --env-file .env build

up:
	docker-compose --env-file .env up -d $(service)

down:
	docker-compose down 

bash:
	docker exec -ti data_ingestion bash

pytest:
	docker exec data_ingestion pytest -p no:warnings -v /data_ingestion/tests/unit

data-ingestion:
	docker exec data_ingestion python data_ingestion.py --dir_config "/input/config/${DATA_INGESTION_CONFIG}"


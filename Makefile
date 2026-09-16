.PHONY: setup data train deploy verify pipeline down airflow-setup airflow

setup:
	./setup_project.sh

data:
	.venv/bin/python code/datasets/prepare_data.py

train:
	.venv/bin/python code/models/train_model.py

deploy:
	docker compose up -d --build

verify:
	.venv/bin/python scripts/verify_deployment.py

pipeline:
	./run_pipeline.sh

down:
	docker compose down

airflow-setup:
	./setup_airflow.sh

airflow:
	./run_airflow.sh

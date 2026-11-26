.PHONY: help infra-up infra-down

.DEFAULT_GOAL := help


help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Available targets:"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)



infra-up: ## start all local backing services (Kafka, MinIO, Redis/Valkey, Postgres, Prometheus, Grafana)
	docker compose -f infra/docker-compose.yaml up -d


infra-down: ## stop all local backing services
	docker compose -f infra/docker-compose.yaml down

infra-verify: ## run health check verification across all backing services
	./infra/verify-health.sh
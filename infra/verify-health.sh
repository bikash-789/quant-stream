#!/usr/bin/env bash
set -e

echo "=========================================="
echo " Checking Platform Infrastructure Health  "
echo "=========================================="

GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m'

check_port() {
  local service=$1
  local host=$2
  local port=$3
  if nc -z "$host" "$port" 2>/dev/null; then
    echo -e " [${GREEN}OK${NC}] $service is reachable on $host:$port"
  else
    echo -e " [${RED}FAIL${NC}] $service is NOT reachable on $host:$port"
  fi
}

check_http() {
  local service=$1
  local url=$2
  if curl -s -f "$url" >/dev/null 2>&1; then
    echo -e " [${GREEN}OK${NC}] $service HTTP endpoint responded healthy ($url)"
  else
    echo -e " [${RED}FAIL${NC}] $service HTTP endpoint did not respond ($url)"
  fi
}

echo ""
echo "1. Kafka Brokers (KRaft Mode):"
check_port "Kafka Broker 1" "localhost" 29092
check_port "Kafka Broker 2" "localhost" 39092
check_port "Kafka Broker 3" "localhost" 49092

echo ""
echo "2. MinIO S3 Object Storage:"
check_port "MinIO API" "localhost" 9000
check_port "MinIO Console" "localhost" 9001
check_http "MinIO Live Health" "http://localhost:9000/minio/health/live"

echo ""
echo "3. Valkey / Redis State Cache:"
check_port "Valkey / Redis" "localhost" 6379

echo ""
echo "4. PostgreSQL + pgvector:"
check_port "PostgreSQL" "localhost" 5432

echo ""
echo "5. Observability (Prometheus & Grafana):"
check_port "Prometheus" "localhost" 9090
check_http "Prometheus Health" "http://localhost:9090/-/healthy"
check_port "Grafana" "localhost" 3000
check_http "Grafana Health" "http://localhost:3000/api/health"

echo ""
echo "++++++++++++++++++++++++++++++++++++++++++"
echo "   Infra Health Check Completed.           "
echo "++++++++++++++++++++++++++++++++++++++++++"

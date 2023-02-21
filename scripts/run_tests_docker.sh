docker compose -f docker-compose-test.yml run --rm api
exit_code=$?
docker compose -f docker-compose-test.yml down --volumes
exit $exit_code
#! /usr/bin/env sh

# Exit in case of error
set -e

DOMAIN=backend \
SMTP_HOST="" \
DATABASE_URL=postgresql://postgres:password@db/app \
TRAEFIK_PUBLIC_NETWORK_IS_EXTERNAL=false \
INSTALL_DEV=true \
docker-compose \
-f docker-compose-unit-test.yml \
config > docker-stack.yml

docker-compose -f docker-stack.yml build
docker-compose -f docker-stack.yml down -v --remove-orphans # Remove possibly previous broken stacks left hanging after an error
docker-compose -f docker-stack.yml up -d
#docker-compose -f docker-stack.yml exec -T backend bash /src/scripts/lint.sh
docker-compose -f docker-stack.yml exec -T backend bash /src/tests-start.sh "$@"
docker-compose -f docker-stack.yml down -v --remove-orphans

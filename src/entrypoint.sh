#!/bin/bash

export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}";
echo ${DATABASE_URL}

case "$PROCESS" in
"LINT")
    mypy . && flake8 . && bandit -r . && safety check
    ;;
"DEV_DJANGO")
    wait_for "${POSTGRES_HOST}" "${POSTGRES_PORT}"
    python manage.py collectstatic --noinput &&
    python manage.py migrate  &&
    uvicorn config.asgi:application --reload-dir apps --debug --host 0.0.0.0 --port 8000 --log-level info --use-colors
#    python manage.py runserver 0.0.0.0:8000
    ;;
"DEV_CELERY")
    wait_for "${BROKER_HOST}" "${BROKER_PORT}"
    celery -A apps.taskapp worker -B --loglevel=INFO --concurrency=1
    ;;
"TEST")
    wait_for "${POSTGRES_HOST}" "${POSTGRES_PORT}"
    pytest -v --cov . --cov-report term-missing --cov-fail-under=100 \
    --color=yes -n 4 --no-migrations --reuse-db -W error
    ;;
"DJANGO")
    wait_for "${POSTGRES_HOST}" "${POSTGRES_PORT}"
    python manage.py collectstatic --noinput &&
    python manage.py migrate
    uvicorn config.asgi:application --reload-dir apps --debug --host 0.0.0.0 --port 8000 --log-level info --use-colors
    ;;
"CELERY")
    wait_for "${BROKER_HOST}" "${BROKER_PORT}"
    echo 'vm.overcommit_memory = 1' >> /etc/sysctl.conf
    case "$NODE" in
    "SCHEDULER")
        celery -A apps.taskapp beat --loglevel=INFO
        ;;
    "CONSUMER")
        celery -A apps.taskapp worker --loglevel=INFO \
        --concurrency=3 --max-tasks-per-child=2048
        ;;
    *)
        echo "NO NODE SPECIFIED!"
        exit 1
        ;;
    esac
    ;;
"FLOWER")
    wait_for "${BROKER_HOST}" "${BROKER_PORT}"
    celery flower \
    --app=apps.taskapp \
    --broker="${CELERY_BROKER_URL}" \
    --basic_auth="${FLOWER_USER}:${FLOWER_PASSWORD}"
    ;;
*)
    echo "NO PROCESS SPECIFIED!"
    exit 1
    ;;
esac

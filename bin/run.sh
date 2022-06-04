#! /bin/bash

case $1 in
    'local') python ./src/main.py;;
    'generate') alembic revision --autogenerate -m $2;;
    'migrate') alembic upgrade heads;;
    'build') docker compose -p fastapi build;;
    # 'start') docker compose -p fastapi up web;;
    'stop') docker compose -p fastapi down;;
    *) echo 'Invalid selection.  Options: build | start'
esac

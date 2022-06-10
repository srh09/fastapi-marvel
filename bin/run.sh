#! /bin/bash

case $1 in
    'local') python ./src/main.py;;
    'generate') alembic revision --autogenerate -m $2;;
    'migrate') alembic upgrade heads;;
    'build') docker compose -p fastapi build;;
    # 'start') docker compose -p fastapi up web;;
    'stop') docker compose -p fastapi down;;
    'truncate')
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'TRUNCATE character CASCADE';
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'TRUNCATE comic CASCADE';
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'TRUNCATE character_comic';
    ;; 
    *) echo 'Invalid selection.  Options: build | start'
esac

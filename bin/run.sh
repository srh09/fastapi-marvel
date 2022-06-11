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
    'drop')
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'DROP TABLE character CASCADE';
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'DROP TABLE comic CASCADE';
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'DROP TABLE character_comic';
    psql -U $POSTGRES_USER -d $POSTGRES_DB -c 'DROP TABLE alembic_version';
    rm -r ./alembic/versions/*
    ;;
    ## rm -rf
    *) echo 'Invalid selection.  Options: local | generate | migrate | build | start | stop | truncate | drop'
esac

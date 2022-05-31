#!/usr/bin/env python
import psycopg2
import os

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_SERVER = os.getenv('POSTGRES_SERVER')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
# DATABASE_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}'
DATABASE_URL = os.getenv('DATABASE_URL')

connection = psycopg2.connect(DATABASE_URL)
cursor = connection.cursor()

cursor.execute("SELECT version();")
version = cursor.fetchone()

connection.close()

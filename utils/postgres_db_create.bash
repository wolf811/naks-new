#!/usr/bin/env bash
sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    CREATE DATABASE naks_site_db;
    CREATE USER naks_site_user WITH PASSWORD 'password';
    ALTER ROLE naks_site_user SET client_encoding TO 'utf8';
    ALTER ROLE naks_site_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE naks_site_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE naks_site_db TO naks_site_user;
    ALTER USER naks_site_user CREATEDB;
EOSQL

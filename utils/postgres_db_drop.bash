#!/usr/bin/env bash
sudo -u postgres psql -v ON_ERROR_STOP=1 --username postgres <<-EOSQL
    DROP DATABASE IF EXISTS naks_site_db;
    DROP DATABASE IF EXISTS test_naks_site_db;
    DROP USER IF EXISTS naks_site_user;
    DROP USER IF EXISTS test_naks_site_db;
EOSQL

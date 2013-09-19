#!/usr/bin/env bash
# exit on errors
set -e

### CONFIG ###
[ -f ".env" ] && source .env

if [ -z "$DB_USER" ]; then
    DB_USER=coop_mes
fi
if [ -z "$DB_PASS" ]; then
    DB_PASS=coop_mes
fi
if [ -z "$DB_NAME" ]; then
    DB_NAME=coop_mes
fi
if [ -z "$DOMAIN" ]; then
    DOMAIN=localhost
fi

PSQL="sudo -u postgres psql"

### FUNCTIONS ###
echo_red() {
    echo -e "\033[31m\033[1m$*\033[0m"
}

install_system_dependencies() {
    echo_red "#######################"
    echo_red "# System Dependencies #"
    echo_red "#######################"
    sudo apt-get -y update

    sudo apt-get -y install make
    sudo apt-get -y install python-virtualenv
    sudo apt-get -y install python-dev
    sudo apt-get -y install postgresql-9.1
    sudo apt-get -y install postgresql-server-dev-9.1
    sudo apt-get -y install postgresql-9.1-postgis
    sudo apt-get -y install libmysqlclient-dev
    sudo apt-get -y install redis-server
    sudo apt-get -y install git
    sudo apt-get -y install mercurial
}

postgres_is_configured() {
    sudo grep '^local\s*all\s*all\s*ident$' \
        /etc/postgresql/9.1/main/pg_hba.conf \
        &> /dev/null
}

configure_postgres() {
    if ! postgres_is_configured; then
        echo_red "######################"
        echo_red "# Configure Postgres #"
        echo_red "######################"
        # change local auth from peer to ident
        sudo sed -i 's/^\(local\s*all\s*all\s*\)peer$/\1ident/' /etc/postgresql/9.1/main/pg_hba.conf
        sudo service postgresql restart
    fi
}

db_user_exists() {
    $PSQL -tAc "SELECT 'ok' FROM pg_roles WHERE rolname='$1'" \
        | grep 'ok' &> /dev/null
}

create_db_user() {
    if ! db_user_exists "${DB_USER}"; then
        echo_red "##################"
        echo_red "# Create DB User #"
        echo_red "##################"
        $PSQL -c "CREATE USER ${DB_USER} PASSWORD '${DB_PASS}';"
    fi
}

db_exists() {
    $PSQL -tAl | grep "^$1" &> /dev/null
}

create_db() {
    if ! db_exists "${DB_NAME}"; then
        echo_red "#############"
        echo_red "# Create DB #"
        echo_red "#############"
        $PSQL -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER} ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C' TEMPLATE template0;"

        # Add postgis
        $PSQL -d ${DB_NAME} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
        $PSQL -d ${DB_NAME} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
        $PSQL -d ${DB_NAME} -c "ALTER TABLE geometry_columns OWNER TO ${DB_USER};"
        $PSQL -d ${DB_NAME} -c "ALTER TABLE spatial_ref_sys OWNER TO ${DB_USER};"
    fi
}

install_app() {
    echo_red "###############"
    echo_red "# Install App #"
    echo_red "###############"

	make install

    ### ??? ###
    $PSQL -d ${DB_NAME} -c "UPDATE django_site SET name='localhost', domain='${DOMAIN}' WHERE id=1;"
    $PSQL -d ${DB_NAME} -c "UPDATE multisite_alias SET domain='${DOMAIN}' WHERE id=1;"
}

### MAIN ###
install_system_dependencies
configure_postgres
create_db_user
create_db
install_app

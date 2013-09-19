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

configure_postgres() {
    echo_red "######################"
    echo_red "# Configure Postgres #"
    echo_red "######################"
    # TODO find a better regexp
    # change auth from peer to ident
    sudo sed -i 's/^local *all *all *peer$/local   all             all                                     ident/' /etc/postgresql/9.1/main/pg_hba.conf
    sudo service postgresql restart
}

create_db_user() {
    echo_red "##################"
    echo_red "# Create DB User #"
    echo_red "##################"
    sudo -u postgres psql -c "CREATE USER ${DB_USER} PASSWORD '${DB_PASS}';"
}

create_db() {
    echo_red "#############"
    echo_red "# Create DB #"
    echo_red "#############"
    sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER} ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C' TEMPLATE template0;"

    # Add postgis
    sudo -u postgres psql -d ${DB_NAME} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
    sudo -u postgres psql -d ${DB_NAME} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
    sudo -u postgres psql -d ${DB_NAME} -c "ALTER TABLE geometry_columns OWNER TO ${DB_USER};"
    sudo -u postgres psql -d ${DB_NAME} -c "ALTER TABLE spatial_ref_sys OWNER TO ${DB_USER};"
}

install_app() {
    echo_red "###############"
    echo_red "# Install App #"
    echo_red "###############"

	make install

    ### ??? ###
    sudo -u postgres psql -d ${DB_NAME} -c "UPDATE django_site SET name='localhost', domain='localhost:8000' WHERE id=1;"
    sudo -u postgres psql -d ${DB_NAME} -c "UPDATE multisite_alias SET domain='localhost:8000' WHERE id=1;"
}

### MAIN ###
install_system_dependencies
configure_postgres
create_db_user
create_db
install_app

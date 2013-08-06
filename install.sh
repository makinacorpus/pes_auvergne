#!/usr/bin/env bash
# exit on errors
set -e

### CONFIG ###
VENV="."
PYTHON="$VENV/bin/python"
PIP="$VENV/bin/pip"

DB_USER=coop_mes
DB_PASS=coop_mes
DB_NAME=coop_mes

echo_green() {
    echo -e "\033[32m\033[1m$*\033[0m"
}

echo_red() {
    echo -e "\033[31m\033[1m$*\033[0m"
}

install_system_dependencies() {
    echo_red "#######################"
    echo_red "# System Dependencies #"
    echo_red "#######################"
    apt-get -y update

    apt-get -y install make
    apt-get -y install python-virtualenv
    apt-get -y install python-dev
    apt-get -y install postgresql-9.1
    apt-get -y install postgresql-server-dev-9.1
    apt-get -y install postgresql-9.1-postgis
    apt-get -y install libmysqlclient-dev
    apt-get -y install redis-server
    apt-get -y install git
    apt-get -y install mercurial
}

configure_postgres() {
    echo_red "######################"
    echo_red "# Configure Postgres #"
    echo_red "######################"
    # TODO find a better regexp
    # change auth from peer to ident
    sed -i 's/^local *all *all *peer$/local   all             all                                     ident/' /etc/postgresql/9.1/main/pg_hba.conf
    service postgresql restart
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

create_virtualenv() {
    echo_red "#####################"
    echo_red "# Create Virtualenv #"
    echo_red "#####################"
    cd $(dirname $VENV)
    virtualenv $(basename $VENV)
    $PIP install -U distribute
}

install_app() {
    echo_red "###############"
    echo_red "# Install App #"
    echo_red "###############"
    ### ??? ###
    $PIP install django==1.4.5 
    $PIP install django-selectable
    $PIP install -e git+git://github.com/makinacorpus/django-coop@django-coop-ionyweb#egg=django-coop
    $PIP install -e git+git://github.com/makinacorpus/ionyweb#egg=ionyweb
    $PIP install simplejson
    $PIP install django-multisite
    $PIP install -e git+git://github.com/makinacorpus/coop-geo@master#egg=coop-geo

    ### ??? ###
    # Modif en cours -------
    $PIP install --exists-action=w -e git+git://github.com/makinacorpus/django-admintools-bootstrap#egg=django-admintools-bootstrap
    $PIP install --exists-action=w -e git+git://github.com/makinacorpus/django-selectable.git@master#egg=django-selectable
    $PIP install --exists-action=w -e git+git://github.com/makinacorpus/django-chosen#egg=django-chosen
    # ----------------------

    $PIP install -r ./requirements.txt

    ### ??? ###
    cp -f ./coop_local/db_settings.py.sample ./coop_local/db_settings.py
    cp -f ./coop_local/local_settings.py.sample ./coop_local/local_settings.py

    sed -i "s/coop_pes_auvergne/$DB_NAME/g" ./coop_local/db_settings.py
    sed -i "s/gisuser/$DB_USER/g" ./coop_local/db_settings.py
    sed -i "s/xxx\+/$DB_PASS/g" ./coop_local/db_settings.py

    ### ??? ###
    mkdir -p ./pes_auvergne_ionyweb/logs

    ### ??? ###
    $PYTHON ./manage.py collectstatic --noinput
    echo_red "/!\\ Name your user 'admin' it's important"
    $PYTHON ./manage.py syncdb --all  # Can't use noinput. Want admin user created
    $PYTHON ./manage.py migrate --fake
    $PYTHON ./manage.py loaddata coop_local/fixtures/*

    ### ??? ###
    $PIP install pillow

    ### ??? ###
    # For ionyweb 
    $PIP uninstall django-tinymce -y
    $PIP install django-tinymce==1.5.1b2

    ### ??? ###
    $PIP install urlobject
    $PIP install django-filebrowser

    ### ??? ###
    $PYTHON ./manage.py syncdb
    $PYTHON ./manage.py migrate

    ### ??? ###
    sudo -u postgres psql -d ${DB_NAME} -c "UPDATE django_site SET name='localhost', domain='localhost:8000' WHERE id=1;"
    sudo -u postgres psql -d ${DB_NAME} -c "UPDATE multisite_alias SET domain='localhost:8000' WHERE id=1;"
}

install_system_dependencies
configure_postgres
create_db_user
create_db
create_virtualenv
install_app

echo_red "Now run $PYTHON manage.py runserver"

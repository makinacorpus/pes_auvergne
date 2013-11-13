Install
=======

System dependencies
-------------------

list of system dependencies:

  - make
  - python-virtualenv
  - python-dev
  - postgresql-9.1
  - postgresql-server-dev-9.1
  - postgresql-9.1-postgis
  - libmysqlclient-dev
  - redis-server
  - git
  - mercurial

with apt::

    apt-get install make python-virtualenv python-dev postgresql-9.1 postgresql-server-dev-9.1 postgresql-9.1-postgis libmysqlclient-dev redis-server git mercurial

Database
--------

Configure postgres to allow utf-8.
In /etc/postgresql/9.1/main/pg_hba.conf, replace::

    local   all             all                                     ident

by::

    local   all             all                                     peer

Then restart postgresql.

In commands::

    $ sudo sed -i 's/^local *all *all *peer$/local   all             all                                     ident/' /etc/postgresql/9.1/main/pg_hba.conf
    $ sudo service postgresql restart

Create a user::

    $ sudo -u postgres psql -c "CREATE USER ${DB_USER} PASSWORD '${DB_PASS}';"

Create a database::

    $ sudo -u postgres psql -c "CREATE DATABASE ${DB_NAME} OWNER ${DB_USER} ENCODING 'UTF8' LC_COLLATE 'C' LC_CTYPE 'C' TEMPLATE template0;"

Install Postgis in the database::

    $ sudo -u postgres psql -d ${DB_NAME} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/postgis.sql
    $ sudo -u postgres psql -d ${DB_NAME} -f /usr/share/postgresql/9.1/contrib/postgis-1.5/spatial_ref_sys.sql
    $ sudo -u postgres psql -d ${DB_NAME} -c "ALTER TABLE geometry_columns OWNER TO ${DB_USER};"
    $ sudo -u postgres psql -d ${DB_NAME} -c "ALTER TABLE spatial_ref_sys OWNER TO ${DB_USER};"

Install application
-------------------

Go in the projet directory::

    $ cd pes_auvergne/

Configure::

    $ cp ./coop_local/db_settings.py.sample ./coop_local/db_settings.py
    $ cp ./coop_local/local_settings.py.sample ./coop_local/local_settings.py

Edit db_settings.py to fill the database credentials.

    $ cp ./pes_cron.sh.sample ./pes_cron.sh
    $ chmod a+x pes_cron.sh

Edit pes_cron.sh to adapt path, then add 2 crontab :
    
    $ crontab -e
    > 5 0 * * * PATH_TO_CRON/pes_cron.sh automatic_validation
    > 5 0 * * * PATH_TO_CRON/pes_cron.sh user_notifications


Install::

    $ make install

Say yes to the admin user creation and name it "admin".


Set the domain::
    $ sudo -u postgres psql -d ${DB_NAME} -c "UPDATE django_site SET name='localhost', domain='localhost:8000' WHERE id=1;"
    $ sudo -u postgres psql -d ${DB_NAME} -c "UPDATE multisite_alias SET domain='localhost:8000' WHERE id=1;"

Run::
    $ ./venv/bin/python manage.py runserver

Go to http://localhost:8000/ to finish the install.

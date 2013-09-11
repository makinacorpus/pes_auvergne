VIRTUALENV=virtualenv
PIP=./venv/bin/pip
PYTHON=./venv/bin/python

default:
	@echo "Read README.rst first"

clean:
	rm -rf Geohash-1.0rc1
	rm -rf build dist

virtualenv: $(PYTHON)
$(PYTHON):
	$(VIRTUALENV) venv
	$(PIP) install -U distribute

requirements: virtualenv
	### ??? ###
	$(PIP) install django==1.4.5
	$(PIP) install django-selectable
	$(PIP) install -e git+git://github.com/makinacorpus/django-coop@django-coop-ionyweb#egg=django-coop
	$(PIP) install -e git+git://github.com/makinacorpus/ionyweb#egg=ionyweb
	$(PIP) install simplejson
	$(PIP) install django-multisite
	$(PIP) install -e git+git://github.com/makinacorpus/coop-geo@master#egg=coop-geo

	### ??? ###
	# Modif en cours -------
	$(PIP) install --exists-action=w -e git+git://github.com/makinacorpus/django-admintools-bootstrap#egg=django-admintools-bootstrap
	$(PIP) install --exists-action=w -e git+git://github.com/makinacorpus/django-selectable.git@master#egg=django-selectable
	$(PIP) install --exists-action=w -e git+git://github.com/makinacorpus/django-chosen#egg=django-chosen
	# ----------------------

	# geohash fails to install from pypi
	tar -xvf Geohash-1.0rc1.tar.gz
	$(PYTHON) Geohash-1.0rc1/setup.py install

	$(PIP) install -r ./requirements.txt

install: requirements
	### ??? ###
	mkdir -p ./pes_auvergne_ionyweb/logs

	### ??? ###
	$(PYTHON) ./manage.py collectstatic --noinput
	$(PYTHON) ./manage.py syncdb --all  # Can't use noinput. Want admin user created
	$(PYTHON) ./manage.py migrate --fake
	$(PYTHON) ./manage.py loaddata coop_local/fixtures/*

	### ??? ###
	$(PIP) install pillow

	### ??? ###
	# For ionyweb
	$(PIP) uninstall django-tinymce -y
	$(PIP) install django-tinymce==1.5.1b2

	### ??? ###
	$(PIP) install urlobject

	### ??? ###
	$(PYTHON) ./manage.py syncdb
	$(PYTHON) ./manage.py migrate

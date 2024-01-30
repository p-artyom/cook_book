WORKDIR = backend
TEMPLATES-DIR = $(WORKDIR)/templates
MANAGE = python $(WORKDIR)/manage.py

run:
	$(MANAGE) runserver

style:
	black -S -l 79 .
	djlint $(TEMPLATES-DIR) --reformat
	isort .
	flake8 .

super:
	$(MANAGE) createsuperuser

makemig:
	$(MANAGE) makemigrations

mig:
	$(MANAGE) migrate

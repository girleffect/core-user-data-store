VENV=./ve
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
FLAKE8=$(VENV)/bin/flake8
PYTEST=$(VENV)/bin/pytest
FLASK=$(VENV)/bin/flask
CODEGEN_VERSION=2.3.1
CODEGEN=java -jar swagger-codegen-cli-$(CODEGEN_VERSION).jar generate
DB_NAME=user_data_store
DB_USER=user_data_store

# Colours.
CLEAR=\033[0m
RED=\033[0;31m
GREEN=\033[0;32m
CYAN=\033[0;36m

.SILENT: docs-build
.PHONY: check test

help:
	@echo "usage: make <target>"
	@echo "    $(CYAN)build-virtualenv$(CLEAR): Creates virtualenv directory, 've/', in project root."
	@echo "    $(CYAN)clean-virtualenv$(CLEAR): Deletes 've/' directory in project root."
	@echo "    $(CYAN)docs-build$(CLEAR): Build documents and place html output in docs root."
	@echo "    $(CYAN)mock-user-data-store-api$(CLEAR): Starts Prism mock server for the User Data Store API."
	@echo "    $(CYAN)validate-swagger$(CLEAR): Check Swagger spec for errors."
	@echo "    $(CYAN)user-data-store-client$(CLEAR): Generate a client for the User Data Store API."
	@echo "    $(CYAN)user-data-store-api$(CLEAN): Generate a Flask server for the User Data Store API."

$(VENV):
	@echo "$(CYAN)Initialise base ve...$(CLEAR)"
	virtualenv $(VENV) -p python3.6
	@echo "$(GREEN)DONE$(CLEAR)"

# Creates the virtual environment.
build-virtualenv: $(VENV)
	@echo "$(CYAN)Building virtualenv...$(CLEAR)"
	# TODO: Depending on project type, requirements will need to be installed here.
	@echo "$(GREEN)DONE$(CLEAR)"

# Deletes the virtual environment.
clean-virtualenv:
	@echo "$(CYAN)Clearing virtualenv...$(CLEAR)"
	rm -rf $(VENV)
	@echo "$(GREEN)DONE$(CLEAR)"

# Build sphinx docs, then move them to docs/ root for GitHub Pages usage.
docs-build:  $(VENV)
	@echo "$(CYAN)Installing Sphinx requirements...$(CLEAR)"
	$(PIP) install sphinx sphinx-autobuild sphinx_rtd_theme
	@echo "$(GREEN)DONE$(CLEAR)"
	@echo "$(CYAN)Backing up docs/ directory content...$(CLEAR)"
	rm -rf docs/source/user_data_store*.rst
	rm -rf docs/source/swagger_server*.rst
	tar -cvf backup.tar docs/source docs/Makefile
	@echo "$(GREEN)DONE$(CLEAR)"
	@echo "$(CYAN)Clearing out docs/ directory content...$(CLEAR)"
	rm -rf docs/
	@echo "$(GREEN)DONE$(CLEAR)"
	@echo "$(CYAN)Restoring base docs/ directory content...$(CLEAR)"
	tar -xvf backup.tar
	@echo "$(GREEN)DONE$(CLEAR)"
	# Remove the tar file.
	rm backup.tar
	# Actually make html from index.rst
	@echo "$(CYAN)Generating sphinx sources...$(CLEAR)"
	$(VENV)/bin/sphinx-apidoc --separate --force -o docs/source/ user_data_store '**/migrations/versions/*.py'
	$(VENV)/bin/sphinx-apidoc --separate --force -o docs/source/ swagger_server
	@echo "$(GREEN)DONE$(CLEAR)"
	@echo "$(CYAN)Generating sphinx docs...$(CLEAR)"
	$(MAKE) -C docs/source clean html SPHINXBUILD=../../$(VENV)/bin/sphinx-build
	@echo "$(GREEN)DONE$(CLEAR)"
	@echo "$(CYAN)Moving build files to docs/ root...$(CLEAR)"
	cp -r docs/_build/html/. docs/
	rm -rf docs/_build/
	@echo "$(GREEN)DONE$(CLEAR)"

swagger-codegen-cli-$(CODEGEN_VERSION).jar:
	wget https://oss.sonatype.org/content/repositories/releases/io/swagger/swagger-codegen-cli/$(CODEGEN_VERSION)/swagger-codegen-cli-$(CODEGEN_VERSION).jar

prism:
	curl -L https://github.com/stoplightio/prism/releases/download/v0.6.21/prism_linux_amd64 -o prism
	chmod +x prism

mock-user-data-store-api: prism
	./prism run --mockDynamic --list -s swagger/user_data_store.yml -p 8083

validate-swagger: prism
	@./prism validate -s swagger/user_data_store.yml && echo "The Swagger spec contains no errors"

$(FLAKE8): $(VENV)
	$(PIP) install flake8

# Generate the flask server code for the User Data Store
user-data-store-api: swagger-codegen-cli-$(CODEGEN_VERSION).jar validate-swagger
	@echo "$(CYAN)Generating flask server for the User Data Store API...$(CLEAR)"
	$(CODEGEN) -i swagger/user_data_store.yml -l python-flask -o .

runserver: $(VENV)
	@echo "$(CYAN)Firing up server...$(CLEAR)"
	$(PYTHON) -m swagger_server

check: $(FLAKE8)
	$(FLAKE8)

$(PYTEST): $(VENV)
	$(PIP) install pytest pytest-cov

test: $(PYTEST)
	$(PYTEST) --verbose --cov=user_data_store --cov=swagger_server/controllers/ user_data_store/ swagger_server/test/

database:
	sql/create_database.sh $(DB_NAME) $(DB_USER) | sudo -u postgres psql -f -
	make migrate

makemigrations: $(VENV)
	@echo "$(CYAN)Creating migrating...$(CLEAR)"
	ALLOWED_API_KEYS="unused" $(VENV)/bin/python manage.py db migrate -d user_data_store/migrations

migrate: $(VENV)
	@echo "$(CYAN)Applying migrations to DB...$(CLEAR)"
	ALLOWED_API_KEYS="unused" $(VENV)/bin/python manage.py db upgrade -d user_data_store/migrations

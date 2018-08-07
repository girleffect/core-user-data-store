"""
IMPORTANT: Changes to this file needs to also reflect in swagger_server.__main__, which
is the entry-point used by uWSGI.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from raven import Client
from raven.contrib.flask import Sentry

from project import settings

APP = Flask(__name__)
CLIENT = Client(
    dsn=settings.SENTRY_DSN,
    processors=(
        "project.processors.SanitizeHeadersProcessor",
    ),
    extra={
        "app": APP,
    }
)
SENTRY = Sentry(client=CLIENT)

APP.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
APP.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

# Initialise sentry
SENTRY.init_app(APP, level=settings.SENTRY_LOG_LEVEL)

DB = SQLAlchemy(APP)

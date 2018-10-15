#!/usr/bin/env python3

import connexion

from flask_sqlalchemy import SQLAlchemy
from raven import Client
from raven.contrib.flask import Sentry
from sqlalchemy.exc import SQLAlchemyError
from ge_core_shared import decorators, exception_handlers, middleware
from prometheus_client import make_wsgi_app
from werkzeug.wsgi import DispatcherMiddleware

from project import settings
from swagger_server import encoder
from swagger_server.controllers import user_data_controller

DB = SQLAlchemy()

metrics = decorators.MetricDecoration([user_data_controller], "core_user_data_store")
metrics.decorate_all_in_modules()

# We create and set up the app variable in the global context as it is used by uwsgi.
app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'User Data API'}, strict_validation=True)

app.app.config["SQLALCHEMY_DATABASE_URI"] = settings.SQLALCHEMY_DATABASE_URI
app.app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = settings.SQLALCHEMY_TRACK_MODIFICATIONS

app.add_error_handler(SQLAlchemyError, exception_handlers.db_exceptions)

# Register middleware
middleware.metric_middleware(app.app, "core_user_data_store")
middleware.auth_middleware(app.app, "core_user_data_store")

DB.init_app(app.app)
CLIENT = Client(
    dsn=settings.SENTRY_DSN,
    processors=(
        "project.processors.SanitizeHeadersProcessor",
    ),
    extra={
        "app": app.app,
    }
)
SENTRY = Sentry(client=CLIENT)
SENTRY.init_app(app.app, level=settings.SENTRY_LOG_LEVEL)
app.app = DispatcherMiddleware(app.app, {
    "/metrics": make_wsgi_app()
})

if __name__ == '__main__':
    app.run(port=8080)

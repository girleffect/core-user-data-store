import connexion
import os

import project.app

orig_environ = dict(os.environ)
orig_environ["ALLOWED_API_KEYS"] = "test-api-key"
os.environ.update(orig_environ)

from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from sqlalchemy.exc import SQLAlchemyError
from ge_core_shared import decorators, exception_handlers, middleware

from swagger_server.encoder import JSONEncoder


DB = SQLAlchemy()


class BaseTestCase(TestCase):

    def create_app(self):
        app = connexion.App(__name__, specification_dir='../swagger/')
        flask_app = app.app
        flask_app.json_encoder = JSONEncoder
        flask_app.config = project.app.APP.config
        flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        DB.init_app(flask_app)
        app.add_error_handler(SQLAlchemyError, exception_handlers.db_exceptions)
        flask_app.wsgi_app = middleware.AuthMiddleware(flask_app.wsgi_app)

        # Register middleware
        middleware.auth_middleware(app.app, "core_user_data_store")
        app.add_api('swagger.yaml', arguments={'title': 'Test User Data API'})
        self.flask_app = flask_app
        return flask_app

    @decorators.db_exception
    def setUp(self):
        super().setUp()
        meta = DB.metadata
        meta.reflect(DB.engine)

        # By reversing the tables, children should get deleted before parents.
        for table in reversed(meta.sorted_tables):
            if table.name == "alembic_version":  # Do not delete migration data
                continue

            DB.session.execute(table.delete())
        DB.session.commit()

    def tearDown(self):
        super().tearDown()
        # Closes all active connections between tests. Prevents session errors
        # bleeding over.
        DB.session.close_all()

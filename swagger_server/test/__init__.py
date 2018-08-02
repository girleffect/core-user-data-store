import connexion
import os

orig_environ = dict(os.environ)
orig_environ["ALLOWED_API_KEYS"] = "test-api-key"
os.environ.update(orig_environ)

from flask_sqlalchemy import SQLAlchemy
from flask_testing import TestCase
from sqlalchemy.exc import SQLAlchemyError
from ge_core_shared import exception_handlers, middleware

from swagger_server.encoder import JSONEncoder

import project.app

from user_data_store import models


DB = SQLAlchemy()

class BaseTestCase(TestCase):

    def create_app(self):
        #logging.getLogger('connexion.operation').setLevel('ERROR')
        app = connexion.App(__name__, specification_dir='../swagger/')
        flask_app = app.app
        flask_app.json_encoder = JSONEncoder
        flask_app.config = project.app.APP.config
        flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        DB.init_app(flask_app)
        app.add_error_handler(SQLAlchemyError, exception_handlers.db_exceptions)
        flask_app.wsgi_app = middleware.AuthMiddleware(flask_app.wsgi_app)
        app.add_api('swagger.yaml', arguments={'title': 'Test User Data API'})
        self.flask_app = flask_app
        return flask_app

    def setUp(self):
        super().setUp()

        # NOTE: TestUserDataController.test_usersitedata_list will fail once
        # super is called. Test makes assumption that there is already data in
        # the db.
        meta = DB.metadata
        meta.reflect(DB.engine)

        # By reversing the tables, children should get deleted before parents.
        for table in reversed(meta.sorted_tables):
            DB.session.execute(table.delete())
        DB.session.commit()

    def tearDown(self):
        super().tearDown()
        # Closes all active connections between tests. Prevents session errors
        # bleeding over.
        DB.session.close_all()

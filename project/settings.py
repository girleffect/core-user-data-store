import os

from user_data_store import mappings, models
import project.app

DEFAULT_API_LIMIT = os.environ.get("DEFAULT_API_LIMIT", 50)
API_KEY_HEADER = "X-API-KEY"
ALLOWED_API_KEYS = set(os.environ["ALLOWED_API_KEYS"].split(","))

# core shared settings
SQLALCHEMY_DB = project.app.DB
ACTION_MODELS = models
ACTION_MAPPINGS = mappings

# sentry settings
SENTRY_DSN = os.environ.get(
    "SENTRY_DSN",
    "https://7026a856f01348ed887633e3b33b0991:8159ab14103b45be90cd491db1317d5e@sentry.io/1188799"
)
SENTRY_LOG_LEVEL = os.environ.get("SENTRY_LOG_LEVEL", logging.ERROR)

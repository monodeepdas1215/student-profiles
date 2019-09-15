from flask import Flask

from app.rest.resource_apis import api as resource_api
from app.rest.auth_api import api as auth_api
from app.utils.config_access import config
from app.utils import logger

flask_app = Flask(__name__)
logger.info("App initialized")

flask_app.config.update(config)
logger.info("App config updated")

# registering the blueprints
flask_app.register_blueprint(resource_api)
flask_app.register_blueprint(auth_api)
logger.info("Blueprints registered")
import flask
from flask_restful import Api
import logging, configparser, os, sys

LOG_LEVEL = logging.DEBUG
LOG_FORMAT = logging.Formatter('%(asctime)s — %(name)s — %(levelname)s — %(funcName)s:%(lineno)d — %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(LOG_FORMAT)
logger.addHandler(stream_handler)

config = configparser.ConfigParser()
# this value is relative to the run.py file
config_path = './SCIM/config.ini'
if os.path.exists(config_path):
    config.read(config_path)
else:
    logger.error('Could not read config file from path %s' % config_path)
    sys.exit(1)

BACKEND_TYPE = config['General']['backend_type']
# init this to False, read from config if the backend is a DB
LOCAL_DATABASE = False
APP_SCHEMA = config['Okta']['schema']

app = flask.Flask(__name__)
app.logger.handlers.clear()
api = Api(app)

if BACKEND_TYPE == 'database':
    from flask_sqlalchemy import SQLAlchemy
    LOCAL_DATABASE = config['Database']['local'].lower() == 'true'
    if LOCAL_DATABASE:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
    else:
        # https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
        app.config['SQLALCHEMY_DATABASE_URI'] = '%s://%s:%s@%s/%s' % (config['Database']['dialect_driver_string'], config['Database']['username'], config['Database']['password'], config['Database']['host'], config['Database']['database'])
    db = SQLAlchemy(app)

from SCIM.endpoints import endpoints
api.add_resource(endpoints.ServiceProviderConfigSCIM, '/ServiceProviderConfigs')
api.add_resource(endpoints.UsersSCIM, '/Users')
api.add_resource(endpoints.UserSpecificSCIM, '/Users/<user_id>')
#api.add_resource(endpoints.GroupsSCIM, '/Groups')
#api.add_resource(endpoints.GroupsSpecificSCIM, '/Groups/<group_id>')
from scripts import consts
from scripts.utils import load_config, load_env_config, extract_last_names
from .common import *
from django.db import connection

CONFIG = load_config(consts.ENV_CONFIG_PATH)
ENV = CONFIG.get("ACTIVE_ENV", )
print(f"System  running in {ENV} environments")

# ##### DEBUG CONFIGURATION
DEBUG = load_env_config("DEBUG", env=ENV, config=CONFIG)

# allow all hosts during development
ALLOWED_HOSTS = load_env_config("ALLOWED_HOSTS", env=ENV, config=CONFIG)

###### APPLICATION CONFIGURATION #########################
NEW_APPS = load_env_config("INSTALLED_APPS", env=ENV, config=CONFIG)
INSTALLED_APPS = DEFAULT_APPS + NEW_APPS

# ##### DATABASE and ROUTERS CONFIGURATION ############################
SCHEMAS = ['public', ] + extract_last_names(NEW_APPS, '.')
DATABASES = load_env_config("DATABASES", env=ENV, config=CONFIG)

#? DATABASES[connection.alias]['OPTIONS'] = {
#     'options': f"-c search_path={','.join(SCHEMAS)}"
# }

#? DATABASE_ROUTERS = load_env_config("DATABASE_ROUTERS", env=ENV, config=CONFIG)

#? PREVIOUSLY_USED_PASSWORD_COUNT = load_env_config("PREVIOUSLY_USED_PASSWORD_COUNT", env=ENV, config=CONFIG)
# This number is in months
# PASSWORD_EXPIRATION_DURATION = load_env_config("PASSWORD_EXPIRATION_DURATION", env=ENV, config=CONFIG)
# PASSWORD_ABOUT_TO_EXPIRE_BEFORE_DAYS = load_env_config("PASSWORD_ABOUT_TO_EXPIRE_BEFORE_DAYS", env=ENV, config=CONFIG)


(EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST,
 EMAIL_HOST_USER, EMAIL_HOST_PASSWORD,
 DEFAULT_FROM_EMAIL, EMAIL_BACKEND) = load_env_config("EMAIL_CONFIG", env=ENV, config=CONFIG).values()


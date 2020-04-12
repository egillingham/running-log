import logging
import json
import os

LOGGER = logging.getLogger("running-log")

secret = os.environ.get("AURORA_CREDS", "{}")
try:
    secret = json.loads(secret)
except Exception as e:
    LOGGER.error(e)

mysql_creds = {
    "host": secret.get("host", "127.0.0.1"),
    "port": secret.get("port", 3306),
    "user": secret.get("username", "root"),
    "password": secret.get("password", "toor")  # toor is only used locally so #yolo let's commit it
}

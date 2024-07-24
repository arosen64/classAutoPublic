import os
from dotenv import load_dotenv

load_dotenv()

USER_ID = os.environ["USER_ID"]
CANVAS_KEY = os.environ["CANVAS_KEY"]
RECEIVER_EMAIL = os.environ["RECEIVER_EMAIL"]
SENDER_EMAIL = os.environ["SENDER_EMAIL"]
USER_PASSWORD = os.environ["USER_PASSWORD"]
CANVAS_HEADER = f'http://jhu.instructure.com/api/v1'
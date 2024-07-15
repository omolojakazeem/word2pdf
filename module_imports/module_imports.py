import logging
import os
import datetime
import time


from dotenv import load_dotenv

load_dotenv()
TELEGRAM_API_KEY = os.getenv("TELEGRAM_API_KEY")
NGROK_URL = os.getenv("NGROK_URL")
PORT = int(os.getenv("PORT", 8080))
SSL_KEY = os.getenv("SSL_KEY")
SSL_CERT = os.getenv("SSL_CERT")
SECRET_TOKEN = os.getenv("SECRET_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


def get_current_datetime_in_ms():
    # Get the current date and time
    now = datetime.datetime.now()
    # Format the date and time to include milliseconds
    formatted_now = now.strftime("%Y%m%d%H%M%S")[:-3]  # Truncate to milliseconds
    return formatted_now



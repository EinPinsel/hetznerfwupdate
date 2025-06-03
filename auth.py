import os
from dotenv import load_dotenv
from requests.auth import HTTPBasicAuth
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Loading environment variables for authentication...")
load_dotenv()

HETZNER_API_URL = os.getenv('HETZNER_API_URL', 'https://robot-ws.your-server.de')
HETZNER_USERNAME = os.getenv('HETZNER_USERNAME')
HETZNER_PASSWORD = os.getenv('HETZNER_PASSWORD')

if not all([HETZNER_USERNAME, HETZNER_PASSWORD]):
    logging.error("Missing Hetzner credentials in environment variables.")
    raise ValueError("Missing Hetzner credentials in environment variables.")

def get_auth():
    logging.info("Providing HTTPBasicAuth object.")
    return HTTPBasicAuth(HETZNER_USERNAME, HETZNER_PASSWORD)

def get_api_url():
    logging.info("Providing Hetzner API URL.")
    return HETZNER_API_URL 
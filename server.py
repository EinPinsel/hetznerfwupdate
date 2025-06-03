import os
from dotenv import load_dotenv
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

logging.info("Loading environment variables for server ID...")
load_dotenv()

HETZNER_SERVER_ID = os.getenv('HETZNER_SERVER_ID')

if not HETZNER_SERVER_ID:
    logging.error("Missing HETZNER_SERVER_ID in environment variables.")
    raise ValueError("Missing HETZNER_SERVER_ID in environment variables.")

def get_server_id():
    logging.info("Providing Hetzner server ID.")
    return HETZNER_SERVER_ID 
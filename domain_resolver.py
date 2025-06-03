import socket
import logging
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def resolve_domain(domain: str = None) -> str:
    if domain is None:
        domain = os.getenv('DOMAIN')
        if not domain:
            logging.error("DOMAIN not set in environment variables.")

    logging.info(f"Resolving domain: {domain}")
    try:
        ip = socket.gethostbyname(domain)
        logging.info(f"Resolved {domain} to IP: {ip}")
        return ip
    except socket.gaierror as e:
        logging.error(f"Failed to resolve domain {domain}: {e}")
        raise 
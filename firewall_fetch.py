import requests
import logging
from auth import get_auth, get_api_url
from server import get_server_id

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def fetch_firewall_rules():
    logging.info("Getting API URL...")
    api_url = get_api_url()
    logging.info("Getting server ID...")
    server_id = get_server_id()
    endpoint = f"/firewall/{server_id}"
    url = f"{api_url}{endpoint}"
    logging.info(f"Built firewall rules URL: {url}")
    auth = get_auth()
    try:
        logging.info(f"Fetching firewall rules from {url}")
        response = requests.get(url, auth=auth, headers={'Content-Type': 'application/x-www-form-urlencoded'}, timeout=10)
        response.raise_for_status()
        logging.info("Firewall rules fetched successfully.")
        return response.json()
    except requests.exceptions.Timeout:
        logging.error("Request timed out after 10 seconds")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {str(e)}")
        raise 
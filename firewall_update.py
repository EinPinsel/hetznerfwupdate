import requests
import logging
import os
import socket
from auth import get_auth, get_api_url
from server import get_server_id
from firewall_fetch import fetch_firewall_rules
from domain_resolver import resolve_domain

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def flatten_rules_for_api(rules):
    data = {}
    for rule_type in ['input', 'output']:
        for idx, rule in enumerate(rules['firewall']['rules'].get(rule_type, [])):
            for key, value in rule.items():
                if value is not None:
                    data[f"rules[{rule_type}][{idx}][{key}]"] = str(value)
    # Optionally add status/whitelist_hos if present
    if 'status' in rules['firewall']:
        data['status'] = rules['firewall']['status']
    if 'whitelist_hos' in rules['firewall']:
        data['whitelist_hos'] = str(rules['firewall']['whitelist_hos']).lower()
    return data

def update_firewall_rules(rules: dict):
    logging.info("Getting API URL...")
    api_url = get_api_url()
    logging.info("Getting server ID...")
    server_id = get_server_id()
    endpoint = f"/firewall/{server_id}"
    url = f"{api_url}{endpoint}"
    logging.info(f"Built firewall update URL: {url}")
    auth = get_auth()

    data = flatten_rules_for_api(rules)
    logging.info(f"Flattened rules for API: {data}")

    try:
        logging.info(f"Updating firewall rules at {url}")
        response = requests.post(
            url,
            auth=auth,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'},
            timeout=10
        )
        response.raise_for_status()
        logging.info("Firewall rules updated successfully.")
        return response.json()
    except requests.exceptions.Timeout:
        logging.error("Request timed out after 10 seconds")
        raise
    except requests.exceptions.RequestException as e:
        logging.error(f"API request failed: {str(e)}")
        raise

# New function to update a rule by name
def update_rule_by_name(rule_name: str, new_rule_data: dict):
    logging.info(f"Updating rule with name: {rule_name}")
    current_rules = fetch_firewall_rules()
    if 'firewall' in current_rules and 'rules' in current_rules['firewall']:
        rules = current_rules['firewall']['rules']
        for rule_type in ['input', 'output']:
            if rule_type in rules:
                for i, rule in enumerate(rules[rule_type]):
                    if rule.get('name') == rule_name:
                        logging.info(f"Found rule '{rule_name}' in {rule_type}. Updating...")
                        rules[rule_type][i].update(new_rule_data)
                        return update_firewall_rules(current_rules)
        logging.warning(f"Rule '{rule_name}' not found.")
    else:
        logging.error("Invalid firewall rules structure.")
    return None

# Function to update a rule based on environment variables
def update_rule_from_env():
    rule_name = os.getenv('RULE_NAME')
    if not rule_name:
        logging.error("RULE_NAME not set in environment variables.")
        return None

    domain = os.getenv('DOMAIN')
    if not domain:
        logging.error("DOMAIN not set in environment variables.")
        return None

    try:
        ip = resolve_domain(domain)
        logging.info(f"Resolved domain {domain} to IP: {ip}")
    except Exception as e:
        logging.error(f"Failed to resolve domain {domain}: {e}")
        return None

    new_rule_data = {
        "ip_version": "ipv4",
        "protocol": "tcp",
        "port": "22",
        "source_ip": f"{ip}/32",
        "action": "accept"
    }

    return update_rule_by_name(rule_name, new_rule_data) 
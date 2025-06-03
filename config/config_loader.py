import yaml
import json

def load_config():
    """
    Loads general app configuration from config/config.yaml.
    """
    with open("config/config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def load_secrets():
    """
    Loads sensitive data (e.g., tokens) from config/secrets.json.
    """
    with open("config/secrets.json", "r") as f:
        return json.load(f)
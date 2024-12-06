import os
import json
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "cli-helper"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "theme": "default",
    "verbose": False,
    "output_format": "text"
}

def ensure_config_dir():
    """Ensure the config directory exists."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_config():
    """Load configuration from file."""
    ensure_config_dir()
    
    if not CONFIG_FILE.exists():
        save_config(DEFAULT_CONFIG)
        return DEFAULT_CONFIG.copy()
    
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    """Save configuration to file."""
    ensure_config_dir()
    
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_config_value(key, default=None):
    """Get a specific configuration value."""
    config = load_config()
    return config.get(key, default)

def set_config_value(key, value):
    """Set a specific configuration value."""
    config = load_config()
    config[key] = value
    save_config(config)

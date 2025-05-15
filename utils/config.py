import yaml
from pathlib import Path

def load_config(config_path: str = "config.yml") -> dict:
    """
    Loads a YAML configuration file and returns its contents as a dictionary.

    Args:
        config_path (str): Path to the YAML configuration file.

    Returns:
        dict: Configuration data.
    """
    config_file = Path(config_path)
    if not config_file.is_file():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    with open(config_file, 'r') as f:
        config = yaml.safe_load(f)
    return config
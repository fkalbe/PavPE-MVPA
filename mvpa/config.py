"""Handle configuration options."""
from pathlib import Path
import yaml


def get_config(filename=None):
    """Load YAML configuration file and return contents as dict."""
    if filename is None:
        project_root = Path(__file__).parents[1]
        filename = project_root / "config.yaml"
    with open(filename) as file:
        return yaml.safe_load(file)

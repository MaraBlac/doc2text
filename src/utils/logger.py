"""
Logging utilities.
"""
import logging
import yaml
import os


def setup_logging(config_path: str = "configs/logging.yaml") -> None:
    """Configure logging based on YAML config."""
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    handler = logging.StreamHandler()
    handler.setLevel(config["root"]["level"])
    handler.setFormatter(logging.Formatter(config["formatters"]["simple"]["format"]))

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def main():
    print("Logger utilities loaded")


if __name__ == "__main__":
    main()

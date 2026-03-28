"""
Configuration loader for YAML config files.
"""
import yaml


def load_config(path: str) -> dict:
    """Load and return configuration."""
    with open(path, "r") as f:
        return yaml.safe_load(f)


def merge_configs(*configs: dict) -> dict:
    """Merge multiple configurations."""
    result = dict(configs[0])
    for config in configs[1:]:
        result.update(config)
    return result


def main():
    config = load_config("configs/pipeline.yaml")
    print(config)


if __name__ == "__main__":
    main()

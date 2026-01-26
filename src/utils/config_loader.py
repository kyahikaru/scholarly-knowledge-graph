import yaml
from pathlib import Path


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_experiment_config(experiment_path: str) -> dict:
    experiment_path = Path(experiment_path)
    experiment_cfg = load_yaml(experiment_path)

    merged_config = {}

    for key, rel_path in experiment_cfg.items():
        cfg_path = (experiment_path.parent / rel_path).resolve()
        merged_config[key] = load_yaml(cfg_path)

    return merged_config

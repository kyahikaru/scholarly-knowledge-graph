import os
import json
import logging
from dataclasses import asdict, is_dataclass

logger = logging.getLogger(__name__)


def cache_exists(path: str) -> bool:
    return os.path.exists(path)


def serialize_item(item):
    if is_dataclass(item):
        return asdict(item)

    if isinstance(item, list):
        return [serialize_item(i) for i in item]

    if isinstance(item, dict):
        return {k: serialize_item(v) for k, v in item.items()}

    return item


def load_cache(path: str):
    logger.info(f"Loading cached data from {path}")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(data, path: str):

    os.makedirs(os.path.dirname(path), exist_ok=True)

    serialized = serialize_item(data)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(serialized, f, indent=2)

    logger.info(f"Saved cache to {path}")

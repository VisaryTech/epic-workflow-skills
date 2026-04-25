#!/usr/bin/env python3
import json
import os
from pathlib import Path

from load_epic_lifecycle import LifecycleError, load_lifecycle

WORKSPACE = Path(__file__).resolve().parents[1]
CONFIG_FILE_PATH = "~/.config/erp-env.json"
CONFIG_PATH = Path(os.path.expanduser(CONFIG_FILE_PATH))
CONFIG_EXAMPLE_PATH = WORKSPACE / "config" / "erp-env.json.example"
BASE_KEYS = [
    "ERP_BASE_URL",
    "ERP_PROJECT_ID",
]


class ConfigError(Exception):
    def __init__(self, reason: str, **extra):
        super().__init__(reason)
        self.reason = reason
        self.extra = extra

    def to_payload(self) -> dict:
        payload = {"ok": False, "reason": self.reason}
        payload.update(self.extra)
        return payload


def normalize(value) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def read_local_config(path: str | Path = CONFIG_FILE_PATH) -> dict:
    config_path = Path(os.path.expanduser(str(path)))
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except Exception as exc:
        raise ConfigError(
            "invalid_config",
            config_path=str(config_path),
            config_example_path=str(CONFIG_EXAMPLE_PATH),
            error=str(exc),
        ) from exc

    if not isinstance(data, dict):
        raise ConfigError(
            "invalid_config",
            config_path=str(config_path),
            config_example_path=str(CONFIG_EXAMPLE_PATH),
            error="config root must be a JSON object",
        )
    return data


def load_known_keys() -> list[str]:
    try:
        lifecycle = load_lifecycle()
    except LifecycleError as exc:
        payload = exc.to_payload()
        payload["config_path"] = str(CONFIG_PATH)
        payload["config_example_path"] = str(CONFIG_EXAMPLE_PATH)
        raise ConfigError(payload.pop("reason"), **payload) from exc

    status_keys = [env_name for env_name in lifecycle["status_env_map"].values()]
    return BASE_KEYS + [lifecycle["plan_epic_label_env"], *status_keys]


def resolve_config_items() -> tuple[list[dict], list[str]]:
    config = read_local_config()
    items = []
    missing = []

    for name in load_known_keys():
        value = normalize(os.getenv(name))
        source = "environment"
        if value is None:
            value = normalize(config.get(name))
            source = "config"
        if value is None:
            missing.append(name)
        items.append({
            "name": name,
            "value": value,
            "source": source if value is not None else None,
        })

    return items, missing


def resolve_env_map() -> tuple[dict[str, str | None], list[str]]:
    items, missing = resolve_config_items()
    return ({item["name"]: item["value"] for item in items}, missing)

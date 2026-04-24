#!/usr/bin/env python3
import json
from pathlib import Path

import yaml

WORKSPACE = Path(__file__).resolve().parents[1]
LIFECYCLE_PATH = WORKSPACE / "docs" / "epic-lifecycle.yaml"


class LifecycleError(Exception):
    def __init__(self, reason: str, **extra):
        super().__init__(reason)
        self.reason = reason
        self.extra = extra

    def to_payload(self) -> dict:
        payload = {"ok": False, "reason": self.reason}
        payload.update(self.extra)
        return payload


def _ensure_mapping(value, field_name: str) -> dict:
    if not isinstance(value, dict):
        raise LifecycleError("invalid_lifecycle_schema", field=field_name)
    return value


def _ensure_list(value, field_name: str) -> list:
    if not isinstance(value, list):
        raise LifecycleError("invalid_lifecycle_schema", field=field_name)
    return value


def load_lifecycle() -> dict:
    try:
        raw = yaml.safe_load(LIFECYCLE_PATH.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise LifecycleError("missing_lifecycle_schema", path=str(LIFECYCLE_PATH), error=str(exc)) from exc
    except yaml.YAMLError as exc:
        raise LifecycleError("invalid_lifecycle_yaml", path=str(LIFECYCLE_PATH), error=str(exc)) from exc

    data = _ensure_mapping(raw, "root")
    statuses_raw = _ensure_list(data.get("statuses"), "statuses")
    markers = _ensure_mapping(data.get("markers"), "markers")
    summaries = _ensure_mapping(data.get("summaries"), "summaries")

    status_order = []
    status_env_map = {}

    for index, item in enumerate(statuses_raw):
        status = _ensure_mapping(item, f"statuses[{index}]")
        key = str(status.get("key", "")).strip()
        label_env = str(status.get("label_env", "")).strip()
        transitions_to = status.get("transitions_to")

        if not key:
            raise LifecycleError("invalid_lifecycle_schema", field=f"statuses[{index}].key")
        if key in status_env_map:
            raise LifecycleError("duplicate_status_key", status=key)
        if not label_env:
            raise LifecycleError("invalid_lifecycle_schema", field=f"statuses[{index}].label_env", status=key)
        if not isinstance(transitions_to, list):
            raise LifecycleError("invalid_lifecycle_schema", field=f"statuses[{index}].transitions_to", status=key)

        normalized_transitions = []
        for target in transitions_to:
            target_key = str(target).strip()
            if not target_key:
                raise LifecycleError(
                    "invalid_lifecycle_schema",
                    field=f"statuses[{index}].transitions_to",
                    status=key,
                )
            normalized_transitions.append(target_key)

        status_order.append(key)
        status_env_map[key] = label_env

    known_statuses = set(status_order)

    for index, item in enumerate(statuses_raw):
        status = item
        key = str(status["key"]).strip()
        for target in status["transitions_to"]:
            target_key = str(target).strip()
            if target_key not in known_statuses:
                raise LifecycleError(
                    "unknown_transition_target",
                    status=key,
                    target=target_key,
                    field=f"statuses[{index}].transitions_to",
                )

    plan_epic_label_env = str(markers.get("plan_epic_label_env", "")).strip()
    if not plan_epic_label_env:
        raise LifecycleError("invalid_lifecycle_schema", field="markers.plan_epic_label_env")

    normalized_summaries = {}
    for name, items in summaries.items():
        if not isinstance(items, list):
            raise LifecycleError("invalid_lifecycle_schema", field=f"summaries.{name}")
        normalized_items = []
        for status in items:
            status_key = str(status).strip()
            if status_key not in known_statuses:
                raise LifecycleError("unknown_summary_status", summary=name, status=status_key)
            normalized_items.append(status_key)
        normalized_summaries[name] = normalized_items

    return {
        "ok": True,
        "path": str(LIFECYCLE_PATH),
        "version": data.get("version", 1),
        "status_order": status_order,
        "status_env_map": status_env_map,
        "plan_epic_label_env": plan_epic_label_env,
        "summaries": normalized_summaries,
    }


def main() -> int:
    try:
        lifecycle = load_lifecycle()
    except LifecycleError as exc:
        print(json.dumps(exc.to_payload(), ensure_ascii=False, indent=2))
        return 1

    print(json.dumps(lifecycle, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import json
import sys
from urllib.parse import urlparse

SUPPORTED_ENTITY_TYPES = {"epic"}
CANONICAL_PATHS = {
    "epic": "/tasktracker/projects/{project_id}/epics/{entity_id}",
}

from erp_config import ConfigError, resolve_env_map


def _resolve_base_url() -> str:
    env_map, _missing = resolve_env_map()
    value = env_map.get("ERP_BASE_URL")
    if not value:
        raise ConfigError("missing_config", missing=["ERP_BASE_URL"])
    return value.rstrip("/")


def _normalize(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = str(value).strip()
    return normalized or None


def _extract_ids_from_epic_url(epic_url: str) -> tuple[str | None, str | None]:
    try:
        path_parts = [part for part in urlparse(epic_url).path.split("/") if part]
    except Exception:
        return None, None

    project_id = None
    epic_id = None
    for index, part in enumerate(path_parts):
        if part == "projects" and index + 1 < len(path_parts):
            project_id = path_parts[index + 1]
        if part == "epics" and index + 1 < len(path_parts):
            epic_id = path_parts[index + 1]
    return project_id, epic_id


def _error_payload(reason: str, entity_type: str | None, entity_id: str | None, project_id: str | None, base_url: str, missing: list[str] | None = None) -> dict:
    return {
        "status": "error",
        "reason": reason,
        "entity_type": entity_type,
        "entity_id": entity_id,
        "project_id": project_id,
        "base_url": base_url,
        "canonical_url": None,
        "missing": missing or [],
    }


def _build_epic_url(base_url: str, entity_id: str | None, project_id: str | None) -> tuple[dict, int]:
    missing = []
    if not entity_id:
        missing.append("entity_id")
    if not project_id:
        missing.append("project_id")

    if missing:
        payload = _error_payload(
            reason="missing_required_parts",
            entity_type="epic",
            entity_id=entity_id,
            project_id=project_id,
            base_url=base_url,
            missing=missing,
        )
        return payload, 1

    payload = {
        "status": "ok",
        "reason": "none",
        "entity_type": "epic",
        "entity_id": entity_id,
        "project_id": project_id,
        "base_url": base_url,
        "canonical_url": f"{base_url}{CANONICAL_PATHS['epic'].format(project_id=project_id, entity_id=entity_id)}",
        "missing": [],
    }
    return payload, 0


def main() -> int:
    try:
        base_url = _resolve_base_url()
    except ConfigError as exc:
        print(json.dumps(exc.to_payload(), ensure_ascii=False, indent=2))
        return 1

    if len(sys.argv) < 3:
        payload = _error_payload(
            reason="usage_error",
            entity_type=None,
            entity_id=None,
            project_id=None,
            base_url=base_url,
            missing=["entity_type", "entity_id"],
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    entity_type = _normalize(sys.argv[1])
    entity_ref = _normalize(sys.argv[2])
    project_id = _normalize(sys.argv[3]) if len(sys.argv) >= 4 else None

    if not entity_type:
        payload = _error_payload(
            reason="missing_entity_type",
            entity_type=None,
            entity_id=entity_ref,
            project_id=project_id,
            base_url=base_url,
            missing=["entity_type"],
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    if entity_type not in SUPPORTED_ENTITY_TYPES:
        payload = _error_payload(
            reason="unsupported_entity_type",
            entity_type=entity_type,
            entity_id=entity_ref,
            project_id=project_id,
            base_url=base_url,
        )
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 1

    entity_id = entity_ref
    if entity_ref and entity_ref.startswith(("http://", "https://")):
        extracted_project_id, extracted_entity_id = _extract_ids_from_epic_url(entity_ref)
        project_id = project_id or extracted_project_id
        entity_id = extracted_entity_id

    payload, code = _build_epic_url(base_url=base_url, entity_id=entity_id, project_id=project_id)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
import json

from erp_config import CONFIG_EXAMPLE_PATH, CONFIG_PATH, ConfigError, resolve_config_items


def main() -> int:
    try:
        items, missing = resolve_config_items()
    except ConfigError as exc:
        print(json.dumps(exc.to_payload(), ensure_ascii=False, indent=2))
        return 1

    payload = {
        "ok": True,
        "result": "envs_loaded",
        "config_path": str(CONFIG_PATH),
        "config_example_path": str(CONFIG_EXAMPLE_PATH),
        "items": items,
        "missing": missing,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

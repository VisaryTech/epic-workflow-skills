#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path

from erp_config import ConfigError, resolve_env_map

WORKSPACE = Path(__file__).resolve().parents[1]
LOAD_LIFECYCLE_SCRIPT = WORKSPACE / "scripts" / "load_epic_lifecycle.py"
CODEX_HOME = Path(os.getenv("CODEX_HOME", Path.home() / ".codex")).resolve()
TASKTRACKER_DIR = CODEX_HOME / "skills" / "tasktracker-api"
PRIORITY_ORDER = [
    ("Priority::1", "P1", 1),
    ("Priority::2", "P2", 2),
    ("Priority::3", "P3", 3),
    ("Priority::4", "P4", 4),
    ("no-priority-label", "без приоритета", None),
]
PAGE_SIZE = 100


def fail(reason: str, **extra):
    payload = {"ok": False, "reason": reason}
    payload.update(extra)
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    raise SystemExit(1)


def parse_input():
    if len(sys.argv) > 1:
        raw = sys.argv[1]
    else:
        raw = sys.stdin.read()
    if not raw.strip():
        return {"mode": "summary", "output": "human"}
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail("invalid_json", error=str(exc))
    data.setdefault("mode", "summary")
    data.setdefault("output", "human")
    return data


def run_json(cmd, cwd=None, reason="report_build_failed"):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    if proc.returncode != 0:
        fail(reason, command=cmd, stderr=proc.stderr.strip(), stdout=proc.stdout.strip())
    text = proc.stdout.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        if text.isdigit():
            return int(text)
        fail("invalid_command_output", command=cmd, stdout=proc.stdout)


def load_lifecycle():
    data = run_json(["python", str(LOAD_LIFECYCLE_SCRIPT)], reason="invalid_lifecycle_schema")
    required_fields = ["status_order", "status_env_map", "plan_epic_label_env", "summaries"]
    missing = [field for field in required_fields if not data.get(field)]
    if missing:
        fail("invalid_lifecycle_schema", missing=missing)
    return data


def load_envs(lifecycle):
    try:
        env_map, _missing = resolve_env_map()
    except ConfigError as exc:
        payload = exc.to_payload()
        fail(payload.pop("reason"), **payload)
    required = [
        "ERP_PROJECT_ID",
        "ERP_BASE_URL",
        lifecycle["plan_epic_label_env"],
        *lifecycle["status_env_map"].values(),
    ]
    missing = [key for key in required if not env_map.get(key)]
    if missing:
        fail("missing_config", missing=missing)
    return env_map


def fetch_epics(project_id, filter_expr):
    epics = []
    skip = 0
    seen_ids = set()

    while True:
        data = run_json(
            [
                "python", "api.py", "-m", "odata_epic",
                "--arg", f"project_id={project_id}",
                "--odata-arg", f"$filter={filter_expr}",
                "--odata-arg", "$select=ID,Title",
                "--odata-arg", "$expand=Labels($select=ID,Title)",
                "--odata-arg", f"$top={PAGE_SIZE}",
                "--odata-arg", f"$skip={skip}",
            ],
            cwd=str(TASKTRACKER_DIR),
            reason="report_build_failed",
        )
        page = data.get("value", [])
        if not isinstance(page, list):
            fail("report_build_failed", detail="invalid_epic_page", skip=skip)

        page_ids = {item.get("ID") for item in page if item.get("ID")}
        duplicate_ids = sorted(epic_id for epic_id in page_ids if epic_id in seen_ids)
        if duplicate_ids:
            fail(
                "report_build_failed",
                detail="duplicate_epic_page",
                skip=skip,
                duplicate_ids=duplicate_ids,
            )

        epics.extend(page)
        seen_ids.update(page_ids)

        if len(page) < PAGE_SIZE:
            break
        skip += PAGE_SIZE

    return epics


def detect_priority(epic):
    labels = epic.get("Labels", []) or []
    label_titles = {item.get("Title") for item in labels if item.get("Title")}
    for raw_name, short_name, _priority_id in PRIORITY_ORDER:
        if raw_name != "no-priority-label" and raw_name in label_titles:
            return raw_name, short_name
    return "no-priority-label", "без приоритета"


def build_priority_groups(epics):
    grouped = {}
    for raw_name, short_name, _priority_id in PRIORITY_ORDER:
        grouped[raw_name] = {
            "name": short_name,
            "count": 0,
            "epics": [],
        }

    for epic in epics:
        raw_name, short_name = detect_priority(epic)
        grouped[raw_name]["name"] = short_name
        grouped[raw_name]["epics"].append({
            "id": epic.get("ID"),
            "title": epic.get("Title") or "(без названия)",
        })

    result = []
    for raw_name, _short_name, _priority_id in PRIORITY_ORDER:
        item = grouped[raw_name]
        item["epics"].sort(key=lambda epic: epic["title"].lower())
        item["count"] = len(item["epics"])
        if item["count"] > 0:
            result.append(item)
    return result


def build_statuses(env_map, lifecycle):
    project_id = env_map["ERP_PROJECT_ID"]
    plan_epic_label_id = env_map[lifecycle["plan_epic_label_env"]]
    statuses = {}
    for status in lifecycle["status_order"]:
        label_id = env_map[lifecycle["status_env_map"][status]]
        filter_expr = (
            f"Labels/any(l:l/ID eq {label_id}) "
            f"and not Labels/any(l:l/ID eq {plan_epic_label_id})"
        )
        epics = fetch_epics(project_id, filter_expr)
        statuses[status] = {
            "count": len(epics),
            "priorities": build_priority_groups(epics),
        }
    return statuses


def build_counts(statuses):
    return {status: item["count"] for status, item in statuses.items()}


def build_totals(counts, lifecycle):
    total = sum(counts.values())
    summaries = lifecycle["summaries"]
    pre_planning = sum(counts.get(status, 0) for status in summaries.get("pre_planning", []))
    planning_pipeline = sum(counts.get(status, 0) for status in summaries.get("planning_pipeline", []))
    ready = sum(counts.get(status, 0) for status in summaries.get("ready", []))
    return {
        "total": total,
        "pre_planning": pre_planning,
        "planning_pipeline": planning_pipeline,
        "ready": ready,
    }


def build_insights(counts, totals):
    insights = []
    if counts:
        top_status, top_count = max(counts.items(), key=lambda item: item[1])
        insights.append(f"Основной объем сейчас в статусе `{top_status}`: {top_count}")
    if totals["ready"] == 0:
        insights.append("Сейчас нет эпиков, готовых к разработке")
    elif totals["ready"] < max(1, totals["total"] // 5):
        insights.append(f"Готовых к разработке эпиков пока немного: {totals['ready']}")
    if counts.get("to-define", 0) > 0:
        insights.append(f"Эпиков, требующих доработки: {counts['to-define']}")
    return insights[:3]


def render_human(report, lifecycle):
    totals = report["totals"]
    insights = report["insights"]
    statuses = report["statuses"]

    lines = []
    lines.append("**Эпики по статусам**")
    for status in lifecycle["status_order"]:
        item = statuses.get(status, {"count": 0, "priorities": []})
        lines.append(f"- `{status}` ({item['count']})")
        if item["count"] == 0:
            lines.append("  - нет эпиков")
            continue
        for priority in item.get("priorities", []):
            lines.append(f"  - `{priority['name']}` ({priority['count']})")
            for epic in priority.get("epics", []):
                epic_id = epic.get("id")
                if epic_id:
                    lines.append(f"    - [{epic_id}] {epic['title']}")
                else:
                    lines.append(f"    - {epic['title']}")

    lines.append("")
    lines.append("**Итого**")
    lines.append(f"- всего: {totals['total']}")
    lines.append(f"- pre_planning: {totals['pre_planning']}")
    lines.append(f"- planning_pipeline: {totals['planning_pipeline']}")
    lines.append(f"- ready: {totals['ready']}")
    if report["mode"] == "full" and insights:
        lines.append("")
        lines.append("**Выводы**")
        for item in insights:
            lines.append(f"- {item}")
    return "\n".join(lines)


def main():
    data = parse_input()
    mode = data.get("mode", "summary")
    output = data.get("output", "human")
    if mode not in {"summary", "full"}:
        fail("unsupported_mode", mode=mode)
    if output not in {"human", "json"}:
        fail("unsupported_output", output=output)

    lifecycle = load_lifecycle()
    env_map = load_envs(lifecycle)
    statuses = build_statuses(env_map, lifecycle)
    counts = build_counts(statuses)
    totals = build_totals(counts, lifecycle)
    insights = build_insights(counts, totals)

    report = {
        "ok": True,
        "result": "report_ready",
        "mode": mode,
        "output": output,
        "counts": counts,
        "statuses": statuses,
        "totals": totals,
        "insights": insights,
    }

    if output == "json":
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print(render_human(report, lifecycle))


if __name__ == "__main__":
    main()

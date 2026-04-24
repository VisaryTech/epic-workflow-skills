---
name: epic-status-report
description: Build human-readable ERP epic workflow reports grouped as status → priority → epic titles, with grouped totals and short management insights. Use for requests like "отчет по статусам эпиков", "статистика эпиков по workflow", "покажи эпики по приоритетам", or "покажи сводку по эпикам".
---

# Epic Status Report

Build a readable report for epic workflow status distribution.

## Входные данные

Optional inputs:
- `mode` (`summary` or `full`)
- `output` (`human` or `json`)

Defaults:
- `mode=summary`
- `output=human`

## ERP-конфиг

- `python scripts/get_erp_envs.py` — canonical ERP config source
- required: `ERP_PROJECT_ID`, `ERP_BASE_URL`, `ERP_LABEL_EPIC_PLAN` и все status-related `ERP_LABEL_*`, определённые в `docs/epic-lifecycle.yaml`

## Источники истины

- `python scripts/get_erp_envs.py` — canonical ERP config source
- `docs/epic-lifecycle.yaml` — canonical lifecycle schema for statuses, labels and summary groups
- `scripts/build_epic_status_report.py` — canonical report builder

## Префлайт

Before execution:
- read ERP config only through `python scripts/get_erp_envs.py`
- require `ERP_PROJECT_ID`, `ERP_BASE_URL`, `ERP_LABEL_EPIC_PLAN` и все status-related `ERP_LABEL_*` из `docs/epic-lifecycle.yaml`
- stop immediately if config is incomplete

## Коды причин

- `missing_config`
- `status_count_failed`
- `report_build_failed`
- `unsupported_mode`
- `unsupported_output`

## Процесс

1. Read ERP config through `python scripts/get_erp_envs.py`.
2. Read lifecycle mapping from `docs/epic-lifecycle.yaml`.
3. Map canonical statuses to ERP label ids.
4. Exclude child plan epics with label `ERP_LABEL_EPIC_PLAN` from the report.
5. For each status, load epics with titles and labels through ERP API, reading all pages instead of truncating the result to the first 100 items.
6. Group epics inside each status by priority.
7. Render each status as `status → priority → epic titles`.
8. Build grouped totals:
   - `total`
   - `pre_planning`
   - `planning_pipeline`
   - `ready`
9. Build short management insights.
10. Return human-readable output by default.
11. Return JSON only when explicitly requested.

## Формат результата

Main script:
- `scripts/build_epic_status_report.py`

Example:

```bash
python scripts/build_epic_status_report.py '{"mode":"full","output":"human"}'
```

Default output is human-readable text.

When `output=json`, return:
- `ok`
- `result: report_ready`
- `mode`
- `output`
- `counts`
- `statuses`
- `totals`
- `insights`

## Ограничения

- Do not perform ERP write operations.
- Do not search labels by title when ERP config is unavailable.
- Prefer human-readable output for chat surfaces.
- Do not include child plan epics with label `ERP_LABEL_EPIC_PLAN` in the top-level epic status report.

## Смоук-чек

- Вход: config неполный → ожидается `missing_config`.
- Вход: `mode=summary`, `output=human` → ожидается человекочитаемый отчет по схеме `status -> priority -> epic titles`.
- Вход: `output=json` → ожидаются поля `counts`, `statuses`, `totals`, `insights`.
- Вход: в ERP есть child plan-epic с `ERP_LABEL_EPIC_PLAN` → ожидается, что он не попадёт в top-level report.
- Вход: в одном статусе больше 100 эпиков → ожидается полный отчёт без усечения первой страницей.

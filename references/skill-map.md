# Epic Skill Map

Use this file when you need a quick routing table for the local epic skill pack.

## Shared Files

- Shared docs live in `docs/`.
- Local epic skills live in `skills/`.

## Child Skills

- `skills/epic-creator`
  Create a new epic in ERP after collecting and validating the required input.
- `skills/epic-deduplicator`
  Remove duplicated content and verbal noise from an ERP epic.
- `skills/epic-refiner`
  Rework an epic after review remarks, especially for `to-define` handling.
- `skills/epic-reviewer`
  Evaluate epic readiness and return the lifecycle decision.
- `skills/epic-dev-plan-creator`
  Build or rebuild the implementation plan as a child ERP epic with label from `ERP_LABEL_EPIC_PLAN`.
- `skills/epic-task-creator`
  Turn an approved child plan epic into ERP development tasks.
- `skills/epic-dev-plan-batch`
  Run planning over a batch of epics selected from ERP.
- `skills/epic-dev-task-batch`
  Run dev-task decomposition over a batch of epics selected from ERP.
- `skills/epic-status-report`
  Build human-readable epic workflow reports.
- `skills/epic-task-weight-estimator`
  Estimate task weights for all tasks linked to an epic.

## External Dependencies

These remain external integrations and are not copied into this repository:

- `tasktracker-api`

ERP config is local to this repository:

- `scripts/get_erp_envs.py`
- `config/erp-env.json`

## Default Decision Order

When intent is ambiguous, choose in this order:
1. `epic-creator`
2. `epic-deduplicator`
3. `epic-reviewer`
4. `epic-refiner`
5. `epic-dev-plan-creator`
6. `epic-task-creator`
7. `epic-status-report`

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
  Turn a child plan epic with `ERP_LABEL_EPIC_PLAN` and `approved` lifecycle marker into ERP development tasks.
- `skills/epic-task-weight-estimator`
  Estimate task weights for all tasks linked to an epic.

## Required Installed Skills

These capabilities are provided by installed skills and are not copied into this repository:

- `visary-cloud-api-skills`
  - use its TaskTracker API capability for ERP TaskTracker read/write operations
  - do not call internal API CLI scripts or rely on its filesystem layout

ERP config is local to this repository:

- `scripts/get_erp_envs.py`
- `~/.config/erp-env.json`

## Default Decision Order

When intent is ambiguous, choose in this order:
1. `epic-creator`
2. `epic-deduplicator`
3. `epic-reviewer`
4. `epic-refiner`
5. `epic-dev-plan-creator`
6. `epic-task-creator`

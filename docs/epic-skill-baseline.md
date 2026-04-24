# Epic Skill Baseline

Короткий operational baseline для skills, которые работают с epic/entity lifecycle, gate markers и ERP side effects.

## Scope

Этот документ описывает общие operational-правила для lifecycle-oriented skills:
- как читать актуальное состояние сущности;
- как трактовать `run status`, `business outcome`, `sync outcome`;
- как работать с gate markers, mismatch и side effects;
- как вести себя при hidden/deleted сущностях.

## Not in scope

Этот документ не определяет:
- lifecycle semantics и допустимые переходы, для этого использовать `docs/epic-workflow.md` и `docs/epic-lifecycle.yaml`;
- readiness-screening перед create/review, для этого использовать `docs/epic-readiness-preflight.md`;
- content quality review, для этого использовать `docs/epic-quality-gates.md`;
- stage-specific required fields, для этого использовать `docs/epic-required-fields.md`.

## Purpose

Этот документ задаёт единые правила исполнения для lifecycle-oriented skills:
- как трактовать результат работы;
- как работать с актуальным состоянием сущности;
- как обрабатывать gate markers, mismatch и side effects;
- как не смешивать business outcome и technical outcome.

## Core terms

- `run status` — технический статус выполнения workflow (`in_progress | done | failed`).
- `business outcome` — предметный результат работы skill, независимый от технических ошибок синхронизации.
- `lifecycle state` — текущее состояние сущности в процессе.
- `lifecycle transition` — целевое изменение состояния сущности.
- `gate marker` — технический маркер допуска или фиксации перехода, не равный lifecycle сам по себе.
- `sync outcome` — результат обязательных side effects и синхронизаций (`done | partial | failed`).
- `completion gates` — минимальный набор проверок, который должен быть пройден до финального success-result.

## Source of truth

- Используй актуальное состояние сущности из системы-источника.
- Не опирайся на старые summaries, предыдущие ответы в чате или старые комментарии как на source of truth.
- Resolver scripts и helper scripts считай каноническим runtime-источником для config, labels, IDs и нормализованных URL.
- Если актуальное состояние нельзя надёжно прочитать, не принимай business decision по устаревшему snapshot.

## Freshness and mismatch

- Перед значимым действием reread текущего состояния обязателен.
- Повторный запуск всегда считается новым запуском.
- Если lifecycle state и gate markers расходятся, skill не должен молча продолжать workflow.
- Если required config, input или gate marker отсутствуют, skill должен явно вернуть stop/fail outcome по своему контракту.

## Hidden entities

- Если ERP-сущность `epic` прочитана с признаком `Hidden = true`, считай её логически удалённой.
- Hidden epic не должен использоваться как активный source/input для review, refine, planning, decomposition, sync или других lifecycle-oriented действий, если пользователь явно не запросил special handling deleted/hidden сущностей.
- Hidden epic не должен учитываться как активный объект при duplicate-check, overlap-check и knowledge-base consistency анализе.
- Если skill reread'ит epic и обнаруживает `Hidden = true`, он должен прервать обычный happy-path и перейти в deleted/hidden handling по своему локальному контракту, а не продолжать workflow как для обычного активного epic.

## Execution discipline

- Явно различай `run status`, `business outcome`, `lifecycle transition` и `sync outcome`.
- Не маскируй technical failure под business verdict.
- Не объявляй success, пока не пройдены обязательные completion gates.
- Если обязательные side effects входят в контракт skill, они должны быть явно попытаны до финального success-response.
- Partial или failed sync нельзя скрывать за обычным success-ответом.
- Вторичные side effects не должны молча откатывать основной результат, если контракт skill явно не требует обратного.

## Authoring rule

- Не дублируй этот baseline длинными пояснениями в каждом `SKILL.md`.
- В локальном skill держи только skill-specific contract, workflow и guardrails.
- Общие operational rules выноси в `/docs`, а не размножай по family-skills.

## Invariants

- no stale reads
- no silent mismatch continuation
- no label/state conflation
- no hidden partial sync
- no success before required gates

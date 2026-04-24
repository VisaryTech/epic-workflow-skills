# Epic Glossary

Словарь терминов для `epic-workflow`.

Используй этот документ, чтобы:
- единообразно писать термины в `docs/`, `SKILL.md` и reference-файлах;
- понимать, какие термины оставлять literal на английском;
- не смешивать несколько вариантов одного и того же понятия в соседних документах.

## Scope

Этот документ определяет:
- preferred wording для ключевых терминов пакета;
- какие термины сохраняются literal;
- какие русские пояснения использовать в обычном тексте.

## Not in scope

Этот документ не определяет:
- lifecycle rules, для этого использовать `docs/epic-workflow.md` и `docs/epic-lifecycle.yaml`;
- style guidance целиком, для этого использовать `docs/epic-writing-style.md`;
- reason-code taxonomy, для этого использовать `docs/epic-reason-codes.md`.

## Usage rules

1. В code-like полях, шаблонах и contract literals сохраняй исходный термин.
2. В обычном поясняющем тексте используй preferred wording из этого словаря.
3. Если термин уже оформлен как literal в backticks, не переводи его внутри этого же вхождения.
4. Не используй несколько конкурирующих переводов одного термина в одном документе.

## Core terms

### `source of truth`
- Preferred in prose: `источник истины`
- Keep literal when:
  - термин используется как устойчивое выражение в шаблоне;
  - термин находится в code-like блоке или checklist literal.
- Avoid:
  - `канонический source`
  - `source of truth по данным`

### `machine-readable`
- Preferred in prose: `машинно-читаемый`
- Keep literal when:
  - термин уже является частью устоявшейся фразы в reference literal.

### `human-readable`
- Preferred in prose: `человекочитаемый`
- Keep literal when:
  - термин фигурирует в literal output contract или template field.

### `run status`
- Preferred in prose: `технический статус выполнения`
- Keep literal when:
  - это имя поля в output/template;
  - это literal enum-like label.

### `business outcome`
- Preferred in prose: `предметный результат`
- Keep literal when:
  - это literal поле или contract term.

### `sync outcome`
- Preferred in prose: `результат синхронизации`
- Keep literal when:
  - это literal поле или contract term.

### `lifecycle state`
- Preferred in prose: `состояние жизненного цикла`
- Keep literal when:
  - термин используется как literal contract field.

### `lifecycle transition`
- Preferred in prose: `переход жизненного цикла`
- Keep literal when:
  - термин используется как literal field name.

### `gate marker`
- Preferred in prose: `технический маркер перехода`
- Keep literal when:
  - термин используется как имя поля;
  - рядом указан конкретный `ERP_LABEL_*`.

### `completion gates`
- Preferred in prose: `обязательные условия завершения`
- Keep literal when:
  - термин уже задан как literal contract phrase.

### `scope`
- Preferred in prose: `границы изменения` или `объём изменения` по контексту
- Keep literal when:
  - речь о placeholder name `` `scope` ``.

### `out-of-scope`
- Preferred in prose: `вне объёма изменения`
- Keep literal when:
  - речь о placeholder name `` `out-of-scope` ``;
  - термин используется в шаблоне.

### `dry-run`
- Preferred in prose: `пробный запуск без записи`
- Keep literal when:
  - это имя флага или literal option.

### `write scope`
- Preferred in prose: `разрешённая область записи`
- Keep literal when:
  - это имя output field или technical label.

### `preflight`
- Preferred in prose: `предварительная проверка`
- Keep literal when:
  - это имя секции `Preflight`;
  - это contract label в skill.

### `reason code`
- Preferred in prose: `код причины`
- Keep literal when:
  - это имя поля `reason code`;
  - речь о literal taxonomy из `docs/epic-reason-codes.md`.

## Style notes

- В обычном русском тексте предпочитай `человекочитаемый` и `машинно-читаемый`, а не английские аналоги.
- В обычном русском тексте предпочитай `источник истины`, а не `source of truth`, если это не literal.
- Для placeholders, enum names и API-like identifiers сохраняй исходные literal значения.

# Epic Workflow

Канонический процесс работы с эпиками: от подготовки требований до готовности к реализации.

`docs/epic-lifecycle.yaml` содержит машинно-читаемую lifecycle schema: status order, transitions, summary groups и mapping `status -> ERP_LABEL_*`.
Этот документ описывает process rules, stage expectations и смысл переходов.
Структуру эпика, required fields, naming, quality gates и reason codes брать из связанных документов в `/docs`.

## Scope

Этот документ определяет:
- смысл lifecycle stages;
- ожидания по стадиям;
- правила переходов между стадиями;
- связь lifecycle и knowledge base consistency gate.

## Not in scope

Этот документ не определяет:
- operational behavior отдельных skills при reread, mismatch, sync и hidden entities, для этого использовать `docs/epic-skill-baseline.md`;
- readiness-screening перед create/review, для этого использовать `docs/epic-readiness-preflight.md`;
- машинно-читаемый lifecycle mapping, для этого использовать `docs/epic-lifecycle.yaml`;
- stage-specific placeholder requirements и content quality review, для этого использовать связанные документы из `/docs`.

## Связанные документы

- `docs/epic-template.md`
- `docs/epic-required-fields.md`
- `docs/epic-quality-gates.md`
- `docs/epic-naming.md`
- `docs/epic-reason-codes.md`
- `docs/epic-lifecycle.yaml`

---

## Модель состояний

Канонические ERP-статусы, их порядок и допустимые переходы определены в `docs/epic-lifecycle.yaml`.
Здесь фиксируются смысл стадий и правила их использования.

---

## Knowledge base consistency gate

Эпик должен быть согласован с материалами из `requirement-source`.

Проверка должна выявлять:
- терминологические расхождения;
- смысловые расхождения;
- scope-расхождения;
- неподтверждённые утверждения;
- противоречия источникам требований.

Проверка обязательна:
- перед переходом `to-approve -> approved`;
- повторно перед planning, если эпик изменялся после review.

---

## Правила переходов

### `draft`
Эпик создан как черновик и находится в стадии первичной подготовки.

На этой стадии:
- допустим intake и последовательное уточнение требований;
- допустима неполная проработка материала для formal review;
- эпик не считается готовым к review автоматически.

Далее, после доведения обязательных полей и readiness baseline, эпик переводится в `to-approve`.

### `to-approve`
Эпик подготовлен и ожидает formal review.

Минимальные ожидания:
- заполнены обязательные поля для стадии согласования;
- понятны бизнес-цель, `to-be-logic`, `scope`, `acceptance-criteria`.

Результат review:
- эпик достаточен → `approved`;
- эпик требует доработки → `to-define`.

Переход `to-approve -> approved` допускается только при успешном прохождении knowledge base consistency gate.

### `to-define`
Эпик или технический план требуют доработки.

После доработки объект возвращается в `to-approve`.

### `approved`
Эпик признан достаточной основой для planning.

На этой стадии:
- сняты критичные gaps и conflicts;
- эпик соответствует общим readiness-требованиям;
- эпик согласован с материалами из `requirement-source`.

Далее агент создаёт дочерний epic технического плана с label, задаваемым через env key `ERP_LABEL_EPIC_PLAN`, после чего этот дочерний epic переводится в `plan-to-approve`.

### `plan-to-approve`
Дочерний epic технического плана с label, задаваемым через env key `ERP_LABEL_EPIC_PLAN`, подготовлен и ожидает проверки TL.

Результат:
- план принят → `plan-approved`;
- план требует доработки → `to-define`.

### `plan-approved`
Дочерний epic технического плана с label, задаваемым через env key `ERP_LABEL_EPIC_PLAN`, утверждён.

Далее агент выполняет декомпозицию, создаёт dev-задачи и связывает их с родительским эпиком и дочерним plan-epic. После этого родительский эпик переводится в `ready`.

### `ready`
Эпик полностью подготовлен к реализации:
- технический план утверждён;
- декомпозиция выполнена;
- dev-задачи созданы.

---

## Lifecycle и ERP labels

Источник истины для lifecycle mapping, status order и summary groups — `docs/epic-lifecycle.yaml`.
ERP labels могут использоваться как технические маркеры, но не заменяют lifecycle.

`ERP_LABEL_EPIC_PLAN` не обозначает lifecycle state. Это типовой маркер, что epic является дочерним technical plan-epic, а не бизнес-эпиком верхнего уровня.

---

## Короткая схема

```text
BA / RP / PM
идея / запрос
      ↓
draft
intake / draft refinement
      ↓
to-approve
formal review + knowledge base consistency gate
      ↓
approved
создание дочернего technical plan-epic
      ↓
plan-to-approve
TL review
      ↓
plan-approved
decomposition
      ↓
ready
```

---

## Правила синхронизации

1. Точка входа в канонический lifecycle — `draft`.
2. Переход в `to-approve` допускается только после доведения эпика до уровня, достаточного для formal review.
3. Решения о полноте и зрелости эпика принимаются по общей базе `/docs`, а lifecycle mapping берётся из `docs/epic-lifecycle.yaml`.
4. Если локальный skill конфликтует с этим workflow или lifecycle schema, нужно обновить skill и/или соответствующий документ так, чтобы сохранить единый источник истины.

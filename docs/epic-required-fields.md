# Обязательные поля эпика

Матрица обязательности placeholder names по стадиям жизненного цикла эпика.

## Scope

Этот документ определяет:
- какие placeholder names обязательны на конкретной стадии;
- какие placeholder names обязательны условно, если контекст эпика этого требует;
- какой минимальный состав полей ожидается для стадии как матрица заполненности.

## Not in scope

Этот документ не определяет:
- lifecycle и transition rules, для этого использовать `docs/epic-workflow.md`;
- severity, blockers и quality gates, для этого использовать `docs/epic-quality-gates.md`;
- preflight-проверку перед create/review, для этого использовать `docs/epic-readiness-preflight.md`.

## Связанные документы
- `docs/epic-template-dictionary.yaml` — source of truth для display labels, enum values и placeholder names;
- `docs/epic-template.md` — форма эпика;
- `docs/epic-workflow.md` — стадии и переходы;
- `docs/epic-quality-gates.md` — quality gates;
- `docs/epic-readiness-preflight.md` — readiness baseline.

---

## Общие правила

1. Обязательность определяется стадией, а не вшивается в сам шаблон эпика.
2. Placeholder считается заполненным только если в нём есть содержательный, проверяемый текст, а не формальная заглушка.
3. Если поле условно обязательно и соответствующий контекст подтверждён, его отсутствие считается незаполненностью для данной стадии.
4. Для integration-case дополнительные требования к спецификации и согласованности проверяются через `docs/epic-readiness-preflight.md` и `docs/epic-quality-gates.md`.

---

## 1. Минимум для создания эпика

### Required placeholders
- `subsystem`
- `module`
- `requirement-source`
- `author`
- `functional-customer`
- `decision-maker`
- `business-goal`

### Conditional placeholders
- нет

### Stage note
Этого минимума достаточно только для осмысленного draft/create-stage, но не для formal review.

---

## 2. Минимум для `to-approve`

### Required placeholders
- `subsystem`
- `module`
- `requirement-source`
- `author`
- `functional-customer`
- `decision-maker`
- `business-goal`
- `problem`
- `expected-effect`
- `to-be-logic`
- `main-scenario`
- `acceptance-criteria`
- `scope`
- `out-of-scope`
- `dependencies`

### Conditional placeholders
- `as-is` — если эпик описывает изменение существующей реализации и без текущего состояния непонятна delta;
- `to-be-rules-and-constraints` — если уже известны существенные правила решения или ограничения;
- `ui-change-area`, `ui-structure`, `ui-display-requirements` — если эпик затрагивает UI/UX;
- `constraints` — если известны ограничения, влияющие на ожидания по решению;
- `risks-and-assumptions` — если уже есть существенные риски, допущения или согласованные рамки;
- `additional-materials` — если без дополнительных материалов нельзя верифицировать входные основания или понять контракт интеграции.

### Stage note
Сама проверка достаточности содержания для перехода выполняется отдельными документами, а этот файл фиксирует только обязательность полей.

---

## 3. Ожидаемая заполненность для `approved`

### Required placeholders
- `subsystem`
- `module`
- `requirement-source`
- `author`
- `functional-customer`
- `decision-maker`
- `business-goal`
- `problem`
- `expected-effect`
- `to-be-logic`
- `main-scenario`
- `acceptance-criteria`
- `scope`
- `out-of-scope`
- `dependencies`

### Conditional placeholders
- `as-is` — когда эпик описывает изменение существующей реализации;
- `to-be-rules-and-constraints` — когда есть существенные правила или ограничения;
- `alternative-scenarios` — когда без них неполны ключевые пользовательские потоки;
- `constraints` — когда ограничения влияют на реализацию, оценку или приёмку;
- `risks-and-assumptions` — когда есть существенные риски, допущения или рамки;
- `ui-change-area`, `ui-structure`, `ui-display-requirements` — при наличии UI scope;
- `additional-materials` — когда без них нельзя проверить основания требований или спецификацию интеграции.

### Stage note
К стадии `approved` обязательные и применимые условные placeholders должны быть проработаны содержательно, а не номинально.

---

## 4. Ожидаемая заполненность для готовности к planning

### Required placeholders
- `to-be-logic`
- `main-scenario`
- `acceptance-criteria`
- `scope`
- `out-of-scope`
- `dependencies`

### Conditional placeholders
- `to-be-rules-and-constraints` — если правила и ограничения влияют на декомпозицию;
- `constraints` — если ограничения влияют на оценку или планирование;
- `risks-and-assumptions` — если риски и допущения влияют на sequencing или solution options;
- `ui-change-area`, `ui-structure`, `ui-display-requirements` — если есть UI scope;
- `additional-materials` — если без дополнительных материалов невозможно корректно спланировать реализацию;
- `as-is` — если без текущего состояния нельзя надёжно спроектировать change.

### Stage note
Этот уровень заполненности нужен для planning и decomposition; transition rules и quality checks определяются отдельными документами.

# Epic Quality Gates

Каталог quality gates для проверки полноты и качества epic content.

## Scope

Этот документ определяет:
- что именно проверять в содержании epic;
- насколько критичен найденный дефект;
- какое корректирующее действие требуется при провале конкретной проверки.

## Not in scope

Этот документ не определяет:
- lifecycle и transition rules, для этого использовать `docs/epic-workflow.md`;
- обязательность placeholder names по стадиям, для этого использовать `docs/epic-required-fields.md`;
- preflight-проверку перед create/review, для этого использовать `docs/epic-readiness-preflight.md`;
- итоговый review verdict, для этого использовать review-specific rules.

## Связанные документы
- `docs/epic-workflow.md`
- `docs/epic-required-fields.md`
- `docs/epic-readiness-preflight.md`
- `epic-reviewer/references/review-checklist.md`

## Severity levels

- `critical` — дефект блокирует следующий значимый переход или делает epic непригодным для надёжной оценки и приёмки.
- `major` — дефект требует доработки, но не всегда блокирует промежуточную проработку.
- `minor` — дефект ухудшает качество формулировок, но сам по себе не блокирует движение.

## Quality gates

### 1. Source clarity
- Проверка: есть ли явный и проверяемый `requirement-source`.
- Severity: `critical`
- Failure action: запросить источник требования или зафиксировать отсутствие основания.

### 2. Change object clarity
- Проверка: понятно ли, что именно меняется или создаётся: подсистема, модуль, объект изменения, функциональная область.
- Severity: `critical`
- Failure action: уточнить объект изменений и область применения.

### 3. Business goal clarity
- Проверка: описаны ли `business-goal`, `problem`, `expected-effect` и не противоречат ли они друг другу.
- Severity: `major`
- Failure action: уточнить бизнес-цель, проблему и ожидаемый эффект.

### 4. To-be logic completeness
- Проверка: описана ли `to-be-logic` на уровне наблюдаемого поведения и бизнес-смысла.
- Severity: `critical`
- Failure action: запросить или доработать целевую логику.

### 5. AS-IS relevance
- Проверка: если эпик описывает изменение существующей реализации, есть ли `as-is` или явное обоснование его отсутствия.
- Severity: `major`
- Failure action: запросить `as-is` или объяснение, почему он не нужен.

### 6. Scenario coverage
- Проверка: есть ли `main-scenario` и, при необходимости, `alternative-scenarios`.
- Severity: `major`
- Failure action: запросить или сформировать пользовательские сценарии.

### 7. Acceptance criteria adequacy
- Проверка: есть ли проверяемые `acceptance-criteria`, описывающие наблюдаемое поведение и результат.
- Severity: `critical`
- Failure action: доработать критерии приёмки до проверяемого вида.

### 8. Scope boundary clarity
- Проверка: определён ли `scope`.
- Severity: `critical`
- Failure action: зафиксировать границы входящего объёма.

### 9. Out-of-scope clarity
- Проверка: определено ли `out-of-scope`.
- Severity: `major`
- Failure action: явно зафиксировать, что не входит в epic.

### 10. UI impact clarity
- Проверка: если epic затрагивает UI/UX, описаны ли `ui-change-area`, `ui-structure`, `ui-display-requirements`.
- Severity: `major`
- Failure action: уточнить UI-зону изменений и требования к отображению.

### 11. Data and entity impact clarity
- Проверка: понятно ли, какие данные, поля, формы, сущности и источники истины затрагиваются.
- Severity: `major`
- Failure action: уточнить данные, сущности и source of truth.

### 12. Dependencies and integrations clarity
- Проверка: зафиксированы ли зависимости, интеграции и внешние системы.
- Severity: `major`
- Failure action: уточнить зависимости, внешние системы и основные ограничения интеграции.

### 12.1 Integration specification clarity
- Проверка: если epic относится к integration-case, указана ли в `requirement-source` и/или `additional-materials` проверяемая спецификация интеграции.
- Severity: `critical`
- Failure action: запросить формализованный контракт интеграции.

### 12.2 Integration specification alignment
- Проверка: если epic описывает доработку существующей интеграции, соответствует ли спецификация текущей реализации.
- Severity: `critical`
- Failure action: актуализировать спецификацию или уточнить текущее состояние до снятия расхождения.

### 13. Constraints clarity
- Проверка: отражены ли существенные ограничения в `constraints` или `to-be-rules-and-constraints`.
- Severity: `major`
- Failure action: уточнить технические, бизнесовые, регуляторные и операционные ограничения.

### 14. Risks and assumptions visibility
- Проверка: отражены ли существенные риски и допущения в `risks-and-assumptions`.
- Severity: `major`
- Failure action: зафиксировать риски, допущения и заранее согласованные рамки.

### 15. Internal consistency
- Проверка: нет ли противоречий между секциями epic.
- Severity: `critical`
- Failure action: остановить продвижение и вернуть список противоречий.

### 16. Knowledge base consistency
- Проверка: согласовано ли содержание epic с материалами из `requirement-source`.
- Severity: `critical`
- Failure action: вернуть список расхождений и требуемых исправлений.

### 17. Non-functional sufficiency
- Проверка: если контекст этого требует, определены ли требования по security, audit, logging, reliability, performance, compliance, SLA.
- Severity: `major`
- Failure action: зафиксировать релевантные non-functional requirements.

### 18. Transition impact clarity
- Проверка: если меняются процесс, роли, статусы, данные или внедрение, описаны ли migration / cutover / enablement requirements.
- Severity: `major`
- Failure action: уточнить переходные требования и условия внедрения.

## General gate rules

1. Любой `critical`-дефект блокирует переход на следующую значимую стадию.
2. Наличие `major`-дефектов требует явной доработки перед согласованием или planning, если дефекты влияют на оценку, приёмку или устойчивость scope.
3. `minor`-дефекты не блокируют движение, если не искажают понимание требований.
4. Для lifecycle-переходов использовать правила из `docs/epic-workflow.md`.
5. Для pre-create и pre-review screening использовать `docs/epic-readiness-preflight.md`.
6. Для formal review использовать deep checklist, а не только этот каталог.

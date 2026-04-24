---
name: epic-refiner
description: "Доработка и редактирование ERP-эпика, в первую очередь эпика с входным lifecycle state или gate marker `to-define`, с повторным чтением актуального epic из ERP по `epicId` или `epicUrl`, выявлением gaps/ambiguities/conflicts, усилением формулировок и acceptance criteria, сохранением согласованных изменений обратно в ERP без изменения меток и статуса эпика. Использовать, когда нужно: доработать epic, исправить замечания после review, заполнить пробелы в требованиях, уточнить acceptance criteria или пересобрать описание эпика без автоматического перевода по lifecycle."
---

# Epic refiner

Доработать ERP-эпик после возврата в `to-define` и подготовить его к повторной подаче на review.

## Входные данные

- `epicId | epicUrl` — идентификатор или URL эпика в ERP.
- optional: замечания review / комментарии BA / PM / TL.
- optional: фокус доработки (`full-refine`, `fill-gaps`, `clarify-ac`, `prepare-recheck`).

## ERP-конфиг

Используй локальный `python scripts/get_erp_envs.py` как единственный канонический источник ERP-конфига.

Обязательное значение для этого skill:
- `ERP_LABEL_TO_DEFINE`

Используй `ERP_LABEL_TO_DEFINE` из ERP config как источник истины для refine gate marker.

## Источники истины

- Общие operational rules: `../../docs/epic-skill-baseline.md`
- Lifecycle and refine gate: `../../docs/epic-workflow.md`, `../../docs/epic-lifecycle.yaml`
- Stage expectations and content checks: `../../docs/epic-required-fields.md`, `../../docs/epic-quality-gates.md`, `../../docs/epic-readiness-preflight.md`
- Epic shape and wording: `../../docs/epic-template.md`, `../../docs/epic-writing-style.md`
- Common reason codes: `../../docs/epic-reason-codes.md`

В этом skill держи только refine-specific контракт.

## Коды причин

- Common reason codes бери из `../../docs/epic-reason-codes.md`.
- Refine-specific preflight case: `epic_not_to_define`.

## Префлайт

Перед доработкой проверь:
- есть `epicId` или `epicUrl`;
- доступен ERP read/update;
- epic существует;
- ERP config успешно получен через `python scripts/get_erp_envs.py`;
- у epic есть lifecycle state `to-define` или expected gate marker из ERP config `ERP_LABEL_TO_DEFINE`, либо пользователь явно запросил override refine-flow;
- доступны `../../docs`, нужные для проверки структуры и readiness baseline.

Если preflight не пройден, заверши run с понятным reason code без частичной записи в ERP.
Если epic не находится в `to-define` и expected gate marker не найден, а override не запрошен явно, возвращай `reason code: epic_not_to_define`.

## Процесс

1. Зафиксируй исходный контекст запроса.
2. Нормализуй вход к `epicId` и заново прочитай актуальный epic из ERP.
3. Получи ERP config через `python scripts/get_erp_envs.py` и проверь refine gate по lifecycle state и expected gate marker `ERP_LABEL_TO_DEFINE`.
4. Проверь epic против `../../docs` и `requirement-source`, включая:
   - недостающие required/conditional blocks, релевантные для текущей стадии;
   - ambiguities, vague wording и internal conflicts;
   - weak / non-testable acceptance criteria;
   - неясные scope / out-of-scope / dependencies / constraints;
   - для change/integration-case: входной screening по `../../docs/epic-readiness-preflight.md` и content-проверки по `../../docs/epic-quality-gates.md`;
   - подтверждённые расхождения с базой знаний.
5. Учти явные замечания из комментариев review, если они переданы или доступны в ERP.
6. Подготовь доработанный текст только в пределах подтверждённого контекста:
   - исправляй только подтверждённые gaps/conflicts;
   - неподтверждённые места выноси в `open_questions` и `remaining_risks`.
7. Сохрани согласованные изменения в ERP без изменения lifecycle state, статуса или gate markers.
8. Верни краткий структурированный итог в чат.

## Формат результата

Возвращай краткий результат со следующими блоками:
- `summary`
- `updated_blocks`
- `open_questions`
- `remaining_risks`
- `ready_for_rereview`

Если integration-case не проходит проверки по `../../docs/epic-readiness-preflight.md` и `../../docs/epic-quality-gates.md`, фиксируй это в `open_questions` и/или `remaining_risks` и не ставь `ready_for_rereview = yes`.

## Ограничения

- Не выдумывай бизнес-факты при нехватке данных.
- Не подменяй требования реализацией.
- Сохраняй intent автора, усиливая ясность и проверяемость.
- Если данных не хватает, формируй `open_questions` вместо догадок.
- Не запускай standard refine-flow без проверки lifecycle state и expected gate marker, если пользователь явно не запросил override.
- Если epic не в `to-define` и expected gate marker не найден, возвращай `reason code: epic_not_to_define`.
- Не записывай в ERP неподтверждённые предположения как факты.
- Не меняй lifecycle state или gate markers автоматически.
- Не подменяй formal review: после доработки epic всё ещё должен пройти повторную проверку.
- Финальный ответ должен быть коротким.

## Смоук-чек

- Вход: epic в `to-define` или с expected gate marker `ERP_LABEL_TO_DEFINE`, подтверждённые gaps исправлены, запись в ERP успешна → ожидается краткий success result с `ready_for_rereview = yes | no` по содержанию.
- Вход: epic не в `to-define`, marker отсутствует и override не запрошен → ожидается `reason code: epic_not_to_define`.
- Вход: данных недостаточно для безопасной доработки → ожидается success/result с заполненными `open_questions` и без неподтверждённых фактов в ERP.

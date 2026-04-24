---
name: epic-dev-task-batch
description: "Пакетная обработка дочерних plan-epic с label ERP_LABEL_EPIC_PLAN и gate ERP_LABEL_PLAN_APPROVED: получает список plan-epic из ERP, для каждого plan-epic вызывает epic-task-creator и формирует единый итоговый отчет по результатам batch-декомпозиции implementation plan в dev-задачи."
---

# Epic Dev Task Batch

## Входные данные

- `epic-task-creator` — локальный дочерний skill для декомпозиции implementation plan в dev-задачи по каждому эпику.

Этот skill не принимает ручной список эпиков. Входной набор всегда получается из ERP как список child plan-epic.

## ERP-конфиг

Используй локальный `python scripts/get_erp_envs.py` как единственный канонический источник ERP-конфига.

Обязательные значения для этого skill:
- `ERP_LABEL_EPIC_PLAN`
- `ERP_LABEL_PLAN_APPROVED`
- `ERP_PROJECT_ID`
- `ERP_BASE_URL`

## Источники истины

- ERP config и список child plan-epic бери из `python scripts/get_erp_envs.py` и ERP API.
- Финальный outcome каждого элемента batch бери только из дочернего `epic-task-creator`.
- Этот skill работает как batch-orchestrator и не подменяет собой decomposition logic дочернего skill.

## Коды причин

- `missing_erp_config`
- `epic_identification_missing`
- `epic_list_fetch_failed`
- `dev_task_batch_failed`

При `missing_erp_config` обязательно приложи список отсутствующих ключей из `python scripts/get_erp_envs.py`, например:
- `ERP_LABEL_EPIC_PLAN`
- `ERP_LABEL_PLAN_APPROVED`
- `ERP_PROJECT_ID`
- `ERP_BASE_URL`

## Префлайт

Перед стартом проверь:
- `ERP_LABEL_EPIC_PLAN`, `ERP_LABEL_PLAN_APPROVED`, `ERP_PROJECT_ID` и `ERP_BASE_URL` успешно получены через `python scripts/get_erp_envs.py`;
- доступен `epic-task-creator`;
- доступно ERP-чтение списка child plan-epic;
- список child plan-epic с gate marker `ERP_LABEL_PLAN_APPROVED` можно получить из ERP;
- для каждого plan-epic можно определить `planEpicId` или `planEpicUrl`.

Если preflight не пройден, верни `❌ failed` с reason code.

## Модель выполнения

Этот skill работает как batch-orchestrator полного run по входному набору эпиков.

Правила выполнения:
- один run = один полный batch по нормализованному входному набору;
- обрабатывай эпики строго последовательно, по одному;
- не запускай следующий эпик, пока предыдущий не получил финальную классификацию;
- batch-run не считается завершённым, пока каждый элемент входного набора не классифицирован как `decomposed`, `needs_attention` или `failed`;
- итоговый batch-report формируй только после завершения полного цикла обработки входного набора;
- локальная ошибка по одному эпику не должна останавливать весь batch, если пользователь явно не попросил stop-on-first-failure.

## Процесс

1. Получи из ERP список child plan-epic с label `ERP_LABEL_EPIC_PLAN` и gate marker `ERP_LABEL_PLAN_APPROVED`.

2. Нормализуй вход:
   - приведи каждый элемент к виду с `planEpicId` и/или `planEpicUrl`;
   - исключи дубли;
   - неидентифицируемые эпики заноси в `failed`.

3. Обрабатывай эпики по одному:
   - для каждого plan-epic отдельно вызывай `epic-task-creator`;
   - не объединяй несколько эпиков в один вызов;
   - не запускай следующий эпик, пока текущий не получил финальный outcome;
   - ошибка по одному эпику не должна останавливать batch, если пользователь не попросил обратного.

4. Зафиксируй результат по каждому эпику:
   - `decomposed` — `epic-task-creator` успешно создал dev-задачи и вернул финальный success outcome;
   - `needs_attention` — `epic-task-creator` вернул финальный неуспешный результат, связанный с содержанием плана, валидацией задач или readiness к `ready`;
   - `failed` — произошла tool/runtime/process ошибка, ответ дочернего skill оборван или итог вызова не определён.

5. Сформируй единый итоговый отчет только после классификации всего входного набора.

## Формат результата

### Человеко-читаемый вывод

Используй короткий человекочитаемый итог без лишних технических деталей.

```md
# Cron // epic-dev-task-batch

Обработано plan-epic: <number>
- Декомпозиция готова: <number>
- Требует внимания: <number>
- Ошибка: <number>

## Что готово
- <planEpicId> — <title>
  - короткий итог
  - создано задач: <number>

## Требует внимания
- <planEpicId> — <title>
  - что именно требует внимания

## Ошибки
- <planEpicId_or_ref> — <краткая причина>
```

Правила:
- не выводи технические поля вроде `result:` и `total_epics:` в человекочитаемом режиме;
- не перегружай отчет списками task id и links, если пользователь не просил полный техотчет;
- не показывай пустые секции;
- детали reason code оставляй только когда они реально помогают понять проблему.

### Структурированный вывод

Если нужен структурированный downstream output, используй поля:
- `total_epics`
- `decomposed`
- `needs_attention`
- `failed`
- `epics[]`
- `failed_items[]`

## Ограничения

- Передавай в `epic-task-creator` только один эпик за вызов.
- Считай результат `epic-task-creator` источником истины и не переписывай созданные задачи, связи и итоговую классификацию без основания в контракте дочернего skill.
- Не выполняй ERP-изменения напрямую в обход `epic-task-creator`.
- Не трактуй старт дочернего skill, промежуточный ответ или частичный ответ как успешное завершение.
- Если completion gates дочернего skill не подтверждены или финальный outcome неоднозначен, не классифицируй эпик как `decomposed`.
- Если ответ дочернего вызова оборван, неоднозначен или не позволяет надёжно определить финальный результат, классифицируй элемент как `failed` или `needs_attention` по контексту.
- Не скрывай частичные ошибки batch-обработки.
- Не останавливай весь batch из-за одной локальной ошибки, если пользователь не попросил stop-on-first-failure.
- Не декомпозируй implementation plan внутри batch-скилла.
- Не создавай задачи напрямую через batch-скилл.
- Не возвращай итоговый batch-report до завершения полного цикла по входному списку.

## Смоук-чек

- Несколько валидных child plan-epic с `ERP_LABEL_EPIC_PLAN` и `ERP_LABEL_PLAN_APPROVED`, все успешно обработаны `epic-task-creator` → `decomposed` совпадает с количеством plan-epic.
- Один вызов `epic-task-creator` завершился содержательной ошибкой, остальные успешны → частично успешный batch-отчет без остановки всего процесса.
- Получение списка эпиков через ERP не удалось → `❌ failed`, `reason code = epic_list_fetch_failed`.
- ERP вернул эпик без достаточной идентификации → элемент попадает в `Failed` с `reason code = epic_identification_missing`.

# Eval cases

Используй эти кейсы для быстрой калибровки и regression-check skill.

## Case 1 — Approved

### Input pattern
Эпик содержит:
- явную business problem;
- цель и measurable outcome;
- stakeholders;
- `scope` / `out-of-scope`;
- `to-be-logic` и сценарии;
- `acceptance-criteria`;
- business rules;
- data/integrations;
- NFR и transition requirements;
- `constraints`, `risks-and-assumptions`, `dependencies`.

### Expected result
- `Готовность: APPROVED_STATUS`
- `Reason: none`
- нет критичных `GAP` и `CONFLICT`

## Case 2 — Missing scope

### Input pattern
Эпик описывает цель и желаемые изменения, но:
- не разделяет `scope` / `out-of-scope`;
- не ограничивает релизный объём;
- содержит расплывчатое перечисление будущих улучшений.

### Expected result
- `Готовность: TO_DEFINE_STATUS`
- `Reason: none`
- минимум один `CRITICAL GAP` в `Scope boundaries`

## Case 3 — Requirements replaced by implementation

### Input pattern
Эпик описывает:
- таблицы БД;
- internal jobs;
- очереди и cron;
- названия endpoint/method/queue;
- но не формулирует business requirements и observable `acceptance-criteria`.

### Expected result
- `Готовность: TO_DEFINE_STATUS`
- `Reason: requirements_replaced_by_implementation`
- замечания в `Stakeholder requirements`, `Functional requirements` и/или `Acceptance criteria`

## Case 4 — Integration epic without specification

### Input pattern
Эпик описывает интеграцию или межсистемный обмен, но:
- в `requirement-source` и `additional-materials` нет проверяемой спецификации;
- нет формализованного контракта, состава данных или правил обмена.

### Expected result
- `Готовность: TO_DEFINE_STATUS`
- `Reason: none`
- `Detail: missing_integration_spec`
- минимум один `CRITICAL GAP` в `Integrations`

## Case 5 — Existing integration change with spec mismatch

### Input pattern
Эпик описывает доработку существующей интеграции, при этом:
- спецификация приложена;
- спецификация расходится с текущей реализацией по контракту, составу данных или направлению обмена.

### Expected result
- `Готовность: TO_DEFINE_STATUS`
- `Reason: none`
- `Detail: integration_spec_mismatch_with_current_implementation`
- замечание минимум уровня `GAP`, а при существенном расхождении `CONFLICT`

## Case 6 — Existing integration change with aligned specification

### Input pattern
Эпик описывает доработку существующей интеграции, при этом:
- в `requirement-source` и/или `additional-materials` есть проверяемая спецификация;
- спецификация согласована с текущей реализацией;
- остальные critical checks пройдены.

### Expected result
- integration-specific blocker не возникает
- epic может получить `APPROVED_STATUS`, если остальные критичные проверки тоже пройдены

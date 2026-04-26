# Readiness rules

Используй этот документ только для decision logic по итогам formal review.

Этот документ отвечает только на вопросы:
- когда вернуть `APPROVED_STATUS`;
- когда вернуть `TO_DEFINE_STATUS`;
- когда вернуть `run status = failed`;
- когда использовать специальные `reason code`.

Этот документ не повторяет полный checklist и не заменяет quality gates.

## Status rules

### Вернуть `APPROVED_STATUS`

Только если одновременно выполняется всё ниже:
- review реально выполнен;
- нет критичных `GAP`;
- нет критичных `CONFLICT`;
- нет критичных `RISK`, делающих объём, границы или приёмку неоценимыми;
- бизнес-проблема, цель и ожидаемый результат сформулированы проверяемо;
- stakeholder requirements понятны и трассируемы;
- title соответствует `Подсистема / Блок_или_Модуль / Функционал` и прошёл naming-check;
- есть устойчивые `scope` / `out-of-scope` boundaries;
- есть `to-be-logic`, `main-scenario` и проверяемые `acceptance-criteria`;
- для integration-case есть проверяемая спецификация;
- для enhancement существующей интеграции спецификация не противоречит текущей реализации;
- зависимости, ограничения и риски позволяют безопасно стартовать разработку.

### Вернуть `TO_DEFINE_STATUS`

Если review реально выполнен и выполняется хотя бы одно из условий:
- есть хотя бы один критичный `GAP`;
- есть хотя бы один критичный `CONFLICT`;
- есть критичный `RISK`, из-за которого нельзя безопасно оценить объём или стартовать работу;
- отсутствует resolved label `ERP_LABEL_TO_APPROVE`;
- требования подменены реализацией в критичных частях epic;
- title не прошёл naming-check и нарушение является критичным для понимания функциональной области, scope или оценки объёма;
- найден `exact_duplicate`;
- найден `strong_overlap` без явного разграничения scope;
- для integration-case отсутствует спецификация интеграции;
- для enhancement существующей интеграции спецификация противоречит текущей реализации.

## Run status rules

### Вернуть `run status = failed`

Если review не был реально выполнен из-за технической или средовой причины:
- не передан `epicId` и нет `epicUrl`;
- epic не удалось прочитать из ERP;
- не удалось resolved обязательные ERP labels/config;
- не определён канал/чат/тред возврата результата.

В этом случае:
- `lifecycle decision = not_evaluated`;
- ERP labels по результату review не обновляются;
- бизнес-вердикт по качеству epic не симулируется.

## Reason code rules

Используй специальные `reason code` только в следующих случаях:
- `missing_epic_ref`;
- `read_epic_failed`;
- `missing_erp_config`;
- `missing_reply_channel`;
- `epic_not_to_approve`;
- `requirements_replaced_by_implementation`;
- `exact_duplicate`;
- `strong_overlap`.

Правило интерпретации:
- `missing_epic_ref`, `read_epic_failed`, `missing_erp_config`, `missing_reply_channel` → `run status = failed`, `lifecycle decision = not_evaluated`;
- `epic_not_to_approve`, `requirements_replaced_by_implementation`, `exact_duplicate`, `strong_overlap` → review завершён, lifecycle decision допускается.

Во всех остальных случаях использовать:
- `Reason: none`

Для integration-case допускается дополнительная диагностическая детализация:
- `Detail: missing_integration_spec`
- `Detail: incomplete_integration_spec`
- `Detail: integration_spec_mismatch_with_current_implementation`

## Criticality rules

Считать замечание `CRITICAL`, если оно влияет на:
- понимание бизнес-проблемы и цели;
- понимание функциональной области из title;
- границы scope и объём релиза;
- проверяемость ключевых требований;
- понимание обязательных зависимостей, ограничений и рисков;
- безопасность, compliance, данные или интеграции для production-контекста;
- внедрение, migration/cutover или безопасный transition.

Считать замечание `NON_CRITICAL`, если оно:
- улучшает полноту, но не блокирует оценку и старт разработки;
- относится к второстепенным уточнениям без влияния на scope/acceptance;
- не меняет итоговый readiness verdict.

## Section roll-up rules

Для сводки по блокам:
- если в блоке есть `CONFLICT`, итог блока = `CONFLICT`;
- иначе если есть `GAP`, итог блока = `GAP`;
- иначе если есть `RISK`, итог блока = `RISK`;
- иначе `OK`;
- `N/A` использовать только если блок реально неприменим к конкретному epic.

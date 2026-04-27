---
name: epic-creator
description: "Пошаговый мастер создания нового epic через чат. Использовать, когда БА или РП хочет собрать обязательные данные, проверить готовность и после подтверждения создать epic в ERP."
---

# Epic Creator

Собрать данные, проверить готовность описания и после подтверждения создать epic в ERP.

## Входные данные

- свободный текст от БА / РП с намерением создать новый epic;
- при наличии: ссылки на ТЗ / ЧТЗ / ТП, схемы, формы, примеры, перечни полей;
- создание epic выполняется через доступный ERP API.

## ERP-конфиг

Используй локальный `python scripts/get_erp_envs.py` как единственный канонический источник ERP-конфига.

Используй результат как источник истины для:
- `ERP_PROJECT_ID`
- `ERP_BASE_URL`
- `ERP_LABEL_DRAFT`

Если конфиг неполный, верни `reason code: missing_erp_config`.

## Источники истины

- Общие operational-правила: `../../docs/epic-skill-baseline.md`
- Intake/create-поток: `../../docs/epic-readiness-preflight.md`, `../../docs/epic-required-fields.md`, `../../docs/epic-workflow.md`
- Структура epic и placeholder names: `../../docs/epic-template.md`, `../../docs/epic-template-dictionary.yaml`
- Content checks, naming-check и стиль формулировок: `../../docs/epic-quality-gates.md`, `../../docs/epic-naming.md`, `../../docs/epic-writing-style.md`
- Common reason codes: `../../docs/epic-reason-codes.md`

В этом skill держи только intake/create-specific контракт. Formal review внутри этого skill не выполняется.

## Коды причин

- Common reason codes бери из `../../docs/epic-reason-codes.md`.
Для диагностической детализации внутри intake допускаются локальные detail reasons:
- `low_source_clarity`
- `unclear_change_object`
- `unclear_scope`
- `codebase_check_required`
- `ambiguous_business_goal`
- `missing_scope_boundaries`
- `missing_acceptance_criteria`
- `cleanup_semantic_drift_detected`
- `cleanup_validation_failed`

Не используй local detail reasons вместо common reason code в финальном результате.

## Префлайт

Перед create-stage проверь:
- входной запрос действительно относится к созданию нового epic;
- доступны нужные документы из `../../docs` для intake и readiness-проверки;
- если пользователь уже просит создание в ERP, ERP config успешно получен через `python scripts/get_erp_envs.py`;
- если пользователь уже просит создание в ERP, доступен ERP API write.

Если preflight не пройден, верни `❌ failed` с common `reason code` без частичного create.

## Процесс

Работай по фазам:

1. **Intake**
   - собери minimum context для нового epic;
   - `author` по умолчанию бери из sender текущего сообщения, если пользователь не указал другого автора;
   - если `requirement-source` отсутствует, зафиксируй это как блокер.

2. **Validate readiness**
   - проверь минимальную обязательность placeholder names для create-stage по `../../docs/epic-required-fields.md`;
   - выполни screening по `../../docs/epic-readiness-preflight.md` и определи исход `not_ready | ready_for_create`;
   - сформируй `Название epic` и `Краткое описание epic`;
   - выполни naming-check по `../../docs/epic-naming.md`;
   - если title не состоит ровно из трёх частей `Подсистема / Блок_или_Модуль / Функционал` или перегружен условиями, деталями, логикой, критериями приёмки либо фразами вида `если`, `при`, `по дате`, `о необходимости`, верни not-ready ответ с `reason: naming_not_stable` в служебной строке;
   - если данных недостаточно для осмысленного создания epic, верни not-ready ответ с common `reason` и при необходимости `detail` в служебной строке.

3. **Optional cleanup before create**
   - если пользователь явно просит очистить текст от воды до создания epic, выполни cleanup в рамках текущего текста без промежуточного сохранения;
   - cleanup не должен менять business intent, обязательные секции и структуру;
   - после cleanup проверь, что не потеряны обязательные поля, acceptance criteria и scope boundaries;
   - если cleanup ухудшил текст или привёл к semantic drift, откати правки и сообщи локальную причину.

4. **Offer next step**
   - перед предложением create явно покажи `Название epic` и `Краткое описание epic`;
   - после успешной проверки готовности предложи только релевантные действия: доработать текст, очистить его от воды или создать epic в ERP;
   - cleanup предлагай по умолчанию как optional шаг, но не запускай без явного запроса или согласия пользователя.

5. **Create epic in ERP**
   - выполняй только после подтверждения пользователя;
   - перед ERP write повторно проверь, что title прошёл naming-check по `../../docs/epic-naming.md`;
   - если title не прошёл naming-check, не выполняй create-stage и верни not-ready ответ с `reason: naming_not_stable` в служебной строке;
   - сначала выполни ERP preflight и получи ERP config через `python scripts/get_erp_envs.py`;
   - используй ERP API;
   - создавай epic без догадок о полях;
   - при создании epic обязательно добавляй label `ERP_LABEL_DRAFT` как стартовую label для lifecycle state `draft`;
   - если `../../docs/epic-workflow.md` фиксирует `draft` как стартовый канонический статус, создавай epic в стартовом lifecycle state `draft`;
   - не выдумывай ERP-статусы и не отклоняйся от канонического lifecycle;
   - если label `ERP_LABEL_DRAFT` не резолвится, не останавливай create-stage;
   - нормализуй ссылку на созданный epic через `python scripts/build_erp_url.py epic <epic_id> <project_id>`.

## Intake guidance

Собирай данные пошагово и только нужными блоками.

Если пользователь просит создать epic, но не дал minimum context или дал только намерение:
- не выводи отдельный список недостающих полей перед шаблоном;
- коротко скажи, что не хватает исходных данных;
- дай блок `Можно прислать одним сообщением по шаблону:`;
- заполняемый шаблон всегда выводи как fenced-блок `text`;
- служебную строку оставляй последней.

Minimum context:
- `subsystem`
- `module`
- `requirement-source`
- `author`
- `functional-customer`
- `decision-maker`
- `business-goal`
- `problem`

Дальше уточняй только релевантные блоки readiness-baseline:
- actors/stakeholders;
- scope + key scenario + `expected-effect`;
- `acceptance-criteria` + `constraints`/`dependencies`;
- при необходимости: UI, data, integrations, workflow/process impact.

Если эпик описывает изменение существующей реализации, не игнорируй `as-is`, если без него непонятна delta.
Если по policy нужен codebase-check, не подменяй отсутствие фактов догадками.

## Формат результата

### Epic not ready
Для business-intake сценариев не начинай ответ с технических полей `status`, `reason code`, `missing`.

Структура ответа:
- человекочитаемый итог: чего не хватает и почему нельзя перейти к create-stage;
- `Название epic` и `Краткое описание epic`, если они уже сформированы; если нет, опускай соответствующую секцию целиком;
- конкретный запрос недостающих данных с русскими названиями из `../../docs/epic-template-dictionary.yaml`;
- короткая служебная строка в конце: `not_ready`, common reason code, placeholder names и local detail reason, если нужен.

Если отсутствует почти весь minimum context, не дублируй недостающие поля списком. Вместо этого используй copy-ready шаблон:

````md
Не хватает исходных данных, чтобы собрать epic для создания.

Можно прислать одним сообщением по шаблону:

```text
Подсистема:
Модуль:
Источник требования:
ФЗ:
ЛПР:
Бизнес-цель:
Проблема:
Границы scope:
Критерии приёмки:
```

Автор эпика я заполню из sender текущего сообщения, если не нужно указать другого.

После этого я соберу заготовку epic.

Служебно: not_ready, reason: missing_input (`subsystem`, `module`, `requirement-source`, `functional-customer`, `decision-maker`, `business-goal`, `problem`)
````

Пример для 1-3 недостающих полей:

```md
Не хватает двух пунктов, чтобы собрать epic для создания.

Название epic:
<canonical_title>

Краткое описание epic:
<short_summary>

Уточните, пожалуйста:
- ФЗ: кто функциональный заказчик
- ЛПР: кто принимает решение по epic

После этого я соберу финальную заготовку для создания epic.

Служебно: not_ready, reason: missing_input (`functional-customer`, `decision-maker`)
```

Для runtime/config/preflight failures, не связанных с business-intake, можно начинать с `❌ failed`, если это быстрее объясняет технический сбой.

### Ready to create

```md
✅ Данные для создания epic готовы.

Название epic:
<canonical_title>

Краткое описание epic:
<short_summary>

Что дальше: доработать описание, очистить текст от воды или создать epic в ERP?
```

### Epic created in ERP

```md
✅ Epic создан: <epic_link>
```

Запрещено выводить:
- полный текст описания в чат;
- длинные пояснения;
- служебные поля вроде `run status`, `comment`, `config`.

## Ограничения

- Не создавай epic в ERP без подтверждения пользователя.
- Не запускай cleanup автоматически без явного запроса или согласия пользователя.
- Cleanup не заменяет formal review и не должен подменять `epic-reviewer`.
- Не выводи полный текст описания epic в чат.
- Не выполняй formal review внутри этого skill.
- Не подменяй отсутствующие требования собственным дизайном.
- При исходе `not_ready` не считай epic готовым к созданию.
- Если title не прошёл naming-check, не создавай epic в ERP.
- Сначала структура названия, потом сохранение в ERP.

## Смоук-чек

- Вход: пользователь просит создать epic без исходных данных или только с намерением → ожидается человекочитаемый not-ready ответ без отдельного списка полей, с copy-ready шаблоном в fenced-блоке `text` и служебной строкой `not_ready, reason: missing_input`.
- Вход: недостаточно данных для `business-goal`, `scope` или `acceptance-criteria` → ожидается человекочитаемый not-ready ответ с `not_ready`, common `reason` в служебной строке и конкретным next step.
- Вход: title `РТ / Словарь терминов / Ведение и согласование` и short summary сформированы, но не хватает `functional-customer`, `decision-maker` → ожидается ответ, который начинается с понятного итога, показывает title/summary, просит ФЗ и ЛПР, а `not_ready, reason: missing_input` вынесен в служебную строку.
- Вход: текст готов к созданию, но пользователь ещё не подтвердил create → ожидается `✅ Данные для создания epic готовы`.
- Вход: title без `/`, из 2/4 частей или с фразами `если`, `при`, `по дате`, `о необходимости` → ожидается not-ready ответ, `reason: naming_not_stable`, без create-stage.
- Вход: title `РТ / Карточка требования / Контроль срока действия` и остальные create-гейты пройдены → ожидается `✅ Данные для создания epic готовы`.
- Вход: пользователь подтвердил создание, ERP write успешен, ссылка нормализована → ожидается `✅ Epic создан: <epic_link>`.
- Вход: пользователь просит cleanup до create, cleanup приводит к semantic drift → ожидается stop/fail без create-stage и без потери исходного intent.

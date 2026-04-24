---
name: epic-reviewer
description: "Проверка готовности эпика к переходу из `to-approve` в `approved` или `to-define` через структурированное review по BABOK-блокам, критическим пробелам, рискам и противоречиям. Использовать, когда нужно: проверить эпик, перепроверить epic/recheck, оценить полноту требований, принять решение APPROVED или TO DEFINE, выявить gaps/conflicts/risks, заново прочитать эпик из ERP и вернуть вердикт с обновлением меток и комментариев."
---

# Epic reviewer

Провести проверку готовности эпика к передаче в разработку.

## Входные данные

- `epicId | epicUrl` — идентификатор или URL эпика в ERP.

Один запуск этого skill обрабатывает только один epic.

## ERP-конфиг

Используй локальный `python scripts/get_erp_envs.py` как единственный канонический источник ERP-конфига.

Ожидай в результате значения:
- `ERP_LABEL_TO_APPROVE`
- `ERP_LABEL_APPROVED`
- `ERP_LABEL_TO_DEFINE`

Если обязательные значения отсутствуют, останавливай preflight с reason code по rules/reference этого skill.

## Источники истины

- Общие operational-правила: `../../docs/epic-skill-baseline.md`
- Lifecycle и семантика стадий: `../../docs/epic-workflow.md`, `../../docs/epic-lifecycle.yaml`
- Required fields и content checks: `../../docs/epic-required-fields.md`, `../../docs/epic-quality-gates.md`, `../../docs/epic-readiness-preflight.md`
- Структура epic и стиль формулировок: `../../docs/epic-template.md`, `../../docs/epic-naming.md`, `../../docs/epic-writing-style.md`
- Common reason codes: `../../docs/epic-reason-codes.md`
Review-specific references, читать по необходимости:
- `references/review-checklist.md`
- `references/readiness-rules.md`
- `references/gotchas.md`
- `references/golden-epic-example.md`
- `references/eval-cases.md`

В этом skill держи только review-specific контракт.

## Коды причин

- Common reason codes бери из `../../docs/epic-reason-codes.md`.
- Review-specific decisioning и mapping preflight/runtime cases бери из `references/readiness-rules.md`.

## Префлайт

Перед review проверь:
- есть `epicId` или `epicUrl`;
- доступно ERP read/update для эпика, labels и комментариев;
- ERP config успешно получен через `python scripts/get_erp_envs.py`;
- доступны нужные `../../docs`;
- определён канал/чат/тред возврата результата.

Если preflight не пройден, заверши run со статусом `failed`, выбери `reason code` по `references/readiness-rules.md` и оформи ответ по шаблону.

Повторная команда на проверку всегда считается новым полным запуском.

## Процесс

1. Зафиксируй исходный контекст запроса: канал/чат/тред.
2. Заново прочитай актуальный epic и его текущее состояние из ERP.
3. Получи ERP config через `python scripts/get_erp_envs.py` и используй результат как источник истины для ERP config values.
4. Проверь входной review gate по `../../docs/epic-workflow.md` и ERP config:
   - epic должен находиться в review-допустимом lifecycle state;
   - expected gate marker `ERP_LABEL_TO_APPROVE` должен присутствовать в ERP config и на epic.
5. Если во входе уже передан `epicUrl`, используй его как ссылку на epic.
6. Оцени epic против `../../docs` и `references/review-checklist.md`, включая:
   - stage expectations и required fields из `../../docs/epic-workflow.md` и `../../docs/epic-required-fields.md`;
   - content quality gates из `../../docs/epic-quality-gates.md`;
   - naming consistency из `../../docs/epic-naming.md`;
   - consistency базы знаний по `requirement-source`;
   - для change/integration-case: входной screening по `../../docs/epic-readiness-preflight.md` и content-проверки по `../../docs/epic-quality-gates.md`;
   - duplicate-check по ERP и knowledge base;
   - спорные случаи через `references/gotchas.md` и итоговое decisioning через `references/readiness-rules.md`.
7. Для каждого замечания укажи статус `OK | GAP | RISK | CONFLICT` и критичность `CRITICAL | NON_CRITICAL`.
   Для integration-case явно фиксируй статус спецификации: `ok | missing | incomplete | conflict` и статус alignment с текущей реализацией: `ok | not_checked | conflict`.
8. Прими итоговый `lifecycle decision`:
   - `approved`
   - `to-define`
   - `not_evaluated` для runtime/preflight/config failure
9. Сформируй full structured result по `assets/review-output-template.md`.
10. Перед ответом в чат попытайся выполнить ERP sync в таком порядке:
   - сначала update gate marker по `lifecycle decision` только через `PATCH /Epic/command/AddLabel/{epicId}`;
   - предыдущий scoped lifecycle label вручную не удаляй, остальные labels не трогай;
   - затем create comment с full structured result;
   - отдельно зафиксируй `erp sync status`, `label sync status/reason`, `comment sync status/reason`.
11. Отправь один итоговый ответ в исходный канал:
   - обычный compact/full result только после попытки ERP sync;
   - если ERP sync завершился как `partial | failed`, явно отрази sync problem;
   - дополнительные интеграционные ошибки не должны скрывать ERP sync status.

## Формат результата

- Используй `assets/review-output-template.md`.
- Для человеко-читаемой структуры и формулировок используй `../../docs/epic-writing-style.md`, если это не противоречит обязательному output template.
- Для ERP-комментария используй full template.
- Для ответа в чат по умолчанию используй compact template без `run status` и `reason code`.
- Full template в чат допустим только если это явно полезно и пользователь не просил скрыть служебные поля.
- Если во входе есть `epicUrl`, поле `Ссылка: <epic_url>` заполняй этим значением.
- Если во входе есть только `epicId` и ссылку корректно определить нельзя, поле `Ссылка:` можно опустить.
- Явно различай `run status`, `lifecycle decision`, `display decision` и `gate marker` в смысле `../../docs/epic-skill-baseline.md` и `../../docs/epic-workflow.md`.
- Поле `Готовность:` всегда заполняй через `display decision`: `APPROVED`, `TO DEFINE` или `not_evaluated`.
- При preflight/config/runtime failure возвращай `run status = failed` и `lifecycle decision = not_evaluated`.
- После review отдельно фиксируй ERP sync outcome (`erp sync status`, `label sync status/reason`, `comment sync status/reason`).
- В ERP всегда записывай full structured result; в чат отправляй итог только после завершения попытки ERP sync.

## Коммуникация

- Не отправляй промежуточные операционные сообщения.
- Не публикуй отдельное `run status: in_progress`, если пользователь не просил live-progress.
- По умолчанию отправляй один итоговый ответ после review или preflight failure.
- Внутренние шаги выполняй молча.
- Если без уточнения нельзя продолжить, задай один короткий вопрос по существу.

## Ограничения

- Не додумывай требования за бизнес.
- Существенную неполноту считай `GAP`, противоречия считай `CONFLICT`.
- Не подменяй review проектированием, архитектурой или реализацией.
- Различай requirement (`что нужно обеспечить`) и design/implementation (`как это будет сделано`).
- Оценивай non-functional и transition requirements по контексту.
- Выполняй проверку consistency базы знаний по `requirement-source` на уровне содержания, а не только структуры.
- Перед фиксацией `scope_mismatch` или `knowledge_base_conflict` нормализуй semantic facts и агрегируй semantic coverage, если source materials декомпозированы по-разному.
- Выполняй duplicate-check по ERP и knowledge base только по полям: `title`, `business-goal`, `to-be-logic`, `main-scenario`, `acceptance criteria`, `subsystem`, `module`.
- Не подменяй lifecycle decision gate marker'ом и не предлагай реализацию/декомпозицию до снятия критичных пробелов.
- Не подменяй formal findings общими советами.
- `scope_mismatch` и `knowledge_base_conflict` фиксируй только после content-based comparison и нормализации semantic facts.
- Не отправляй обычный business verdict в чат, если ERP sync не был попытан.
- Не скрывай `erp sync status = partial | failed` за обычным compact-ответом.
- Для `lifecycle decision = approved | to-define` comment create в ERP нужен до ответа в чат.
- При `run status = failed` не меняй lifecycle decision и ERP gate markers.
- Не использовать `ChangeLabels` для lifecycle/status scoped labels и не пересобирать полный список labels ради смены lifecycle marker.
- При любых label update не сноси несвязанные labels, например priority, ownership, service labels и другие non-lifecycle markers.
- Если запуск был не в основном пользовательском диалоге, всё равно доставь итог в исходный канал.

## Смоук-чек

Детальные eval-кейсы и расширенные smoke scenarios см. в `references/eval-cases.md`.

Минимум ожидается следующее:
- Эпик без expected gate marker `ERP_LABEL_TO_APPROVE` → `run status = done`, `lifecycle decision = to-define`, `reason code = epic_not_to_approve`.
- Эпик с критичным `GAP` или `CONFLICT` → `run status = done`, `lifecycle decision = to-define`.
- Полный и проверяемый эпик без критичных замечаний + label sync ok + comment sync ok → `run status = done`, `lifecycle decision = approved`, `erp sync status = done`.
- Review done + `label sync failed` или `comment sync failed` → `erp sync status = partial | failed`, итоговый чат-ответ явно отражает sync failure.

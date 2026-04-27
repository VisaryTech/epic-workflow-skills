# Epic Reason Codes

Единый справочник reason codes для skill, связанных с жизненным циклом эпика.

## Общие правила

- Использовать `lower_snake_case`.
- Один код = одна чёткая причина.
- Не смешивать в одном code и симптом, и решение.
- Если причина блокирует переход на следующую стадию, это должно быть отражено в workflow skill.

## Intake / create

- `missing_input` — не хватает обязательных входных данных.
- `insufficient_input_for_create` — данных недостаточно даже для осмысленного описания эпика.
- `naming_not_stable` — невозможно собрать корректное и предметное название.
- `source_not_provided` — не указан источник требования.
- `missing_erp_config` — отсутствует обязательный ERP config для create flow.
- `epic_create_failed` — не удалось создать эпик в ERP.

## Review

- `missing_epic_ref` — не передан `epicId` и нет `epicUrl` для review.
- `read_epic_failed` — не удалось прочитать эпик из ERP.
- `missing_reply_channel` — не определён канал/чат/тред возврата результата.
- `epic_not_to_approve` — эпик не находится в состоянии / с label, допускающем review.
- `missing_labels_config` — не хватает обязательного label/config для review.
- `requirements_replaced_by_implementation` — требования подменены реализацией.
- `critical_gap` — найден критичный пробел, блокирующий продвижение.
- `critical_conflict` — найдено критичное противоречие.
- `insufficient_for_approval` — эпик в целом недостаточно зрелый для `approved`.
- `missing_requirement_source` — отсутствует или недостаточно заполнено поле `requirement-source` для проверки по базе знаний.
- `term_mismatch` — термин в эпике не совпадает с термином из материалов `requirement-source`.
- `term_inconsistency` — одна и та же сущность названа по-разному внутри эпика.
- `wording_mismatch` — формулировка эпика меняет или размывает смысл материала из `requirement-source`.
- `knowledge_base_gap` — в эпике есть утверждение, не подтверждённое материалами из `requirement-source`.
- `knowledge_base_conflict` — содержание эпика противоречит материалам из `requirement-source`.
- `scope_mismatch` — scope эпика не совпадает со scope, зафиксированным в материалах `requirement-source`.
- `exact_duplicate` — epic дублирует уже существующий epic или материал базы знаний.
- `strong_overlap` — epic существенно пересекается с существующим epic или материалом базы знаний без явного разграничения scope.

## Planning

- `missing_epic_ref` — не передан `epicId` или `epicUrl`.
- `epic_not_approved` — эпик не готов к planning.
- `plan_epic_create_failed` — не удалось создать дочерний plan-epic в ERP.
- `plan_epic_update_failed` — не удалось обновить дочерний plan-epic в ERP.
- `epic_comment_failed` — не удалось оставить обязательный комментарий в ERP.

## Decomposition

- `missing_plan_ref` — не передан `epicId`, `planEpicId` или `planEpicUrl`.
- `plan_not_found` — дочерний plan-epic отсутствует или пуст.
- `epic_plan_not_approved` — дочерний plan-epic с `ERP_LABEL_EPIC_PLAN` не имеет lifecycle marker/status `approved`.
- `code_alignment_failed` — декомпозиция не согласуется с текущей реализацией.
- `task_validation_failed` — задачи не проходят обязательную валидацию.
- `tasks_create_failed` — не удалось создать задачи в ERP.
- `links_create_failed` — не удалось создать связи между задачами.
- `links_verify_failed` — нет подтверждения созданных связей.
- `done_label_set_failed` — не удалось установить финальный label стадии декомпозиции.

## Usage note

Если skill использует свои локальные decision rules, они не должны противоречить этому документу. При расхождении приоритет у общей базы `/docs`.

Для review-workflow дополнительно различать:
- technical run failure — review не выполнен, `lifecycle decision = not_evaluated`;
- lifecycle decision — review выполнен и вынесен вердикт `approved | to-define`.

Коды `missing_epic_ref`, `read_epic_failed`, `missing_labels_config`, `missing_reply_channel` по умолчанию относятся к technical run failure, а не к business verdict по качеству эпика.

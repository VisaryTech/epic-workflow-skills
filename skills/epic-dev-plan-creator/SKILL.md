---
name: epic-dev-plan-creator
description: "Использовать, когда нужно подготовить план реализации по одному эпику. Применять для запросов вида «сделай план по эпику/epicId», «пересоздай план эпика», «обнови план эпика»."
---

# Epic Dev Plan Creator

## Входные данные

- `epicId | epicUrl` — идентификатор или URL эпика в ERP.
- один запуск этого skill подготавливает план только для одного epic;
- не принимать несколько epic в одном запуске.

## ERP-конфиг

Используй локальный `python scripts/get_erp_envs.py` как единственный канонический источник ERP-конфига.

Обязательные значения для этого skill:
- `ERP_LABEL_APPROVED`
- `ERP_LABEL_EPIC_PLAN`

Если обязательные значения отсутствуют, останавливай preflight с reason code этого skill.

## Модель плана

- implementation plan хранится в ERP как дочерний epic;
- дочерний epic плана обязан иметь label `ERP_LABEL_EPIC_PLAN`;
- готовность плана к декомпозиции подтверждается обычным lifecycle marker `approved` через `ERP_LABEL_APPROVED` на дочернем plan-epic;
- source of truth для текста плана — описание этого дочернего epic.
- для одного родительского epic должен использоваться один canonical child plan-epic; дубликаты не создавать.

## Источники истины

- Общие operational-правила: `../../docs/epic-skill-baseline.md`
- Planning gate и lifecycle-семантика: `../../docs/epic-workflow.md`, `../../docs/epic-lifecycle.yaml`
- Stage expectations и content blockers: `../../docs/epic-required-fields.md`, `../../docs/epic-quality-gates.md`
- Структура epic и стиль формулировок: `../../docs/epic-template.md`, `../../docs/epic-writing-style.md`
- Common reason codes: `../../docs/epic-reason-codes.md`

В этом skill держи только planning-specific контракт.

## Коды причин

- Common reason codes бери из `../../docs/epic-reason-codes.md`.
- Локальные planning-specific дополнения для этого skill:
- `previous_plan_not_found`
- `plan_epic_create_failed`
- `plan_epic_update_failed`

## Префлайт

Перед стартом workflow проверь:
- есть `epicId` или `epicUrl`;
- ERP config успешно получен через `python scripts/get_erp_envs.py`;
- доступны общие документы `../../docs`, необходимые для planning;
- доступны права на создание или обновление дочернего epic в ERP.

Дополнительно:
- epic должен иметь expected gate marker `ERP_LABEL_APPROVED`.

Если preflight не пройден, верни `❌ failed` с reason code.

## Процесс

1. Прими входной `epicId` или `epicUrl` и получи ERP config через `python scripts/get_erp_envs.py`.
2. Прочитай актуальный epic из ERP и используй его как источник истины по бизнес-смыслу и scope.
3. Проверь readiness к planning по `../../docs`: lifecycle gate через `../../docs/epic-workflow.md`, stage expectations через `../../docs/epic-required-fields.md`, content blockers через `../../docs/epic-quality-gates.md`, и expected gate marker `ERP_LABEL_APPROVED`.
4. Перед анализом проверь, что локальный workspace содержит актуальные релевантные кодовые репозитории и доступен для чтения.
5. Выполни поиск текущей реализации в релевантных локальных кодовых репозиториях с учётом локального контекста и repo-local инструкций.
6. Зафиксируй результат поиска как часть planning basis:
   - `existing implementation: found`
   - `existing implementation: not found`
   - `existing implementation: not identified`
7. Если реализация не найдена или не идентифицирована, фиксируй результат поиска и основания вывода, но не классифицируй это автоматически как риск.
8. Подготовь canonical implementation plan как текст дочернего ERP epic.
9. Найди существующий дочерний plan-epic по связи с родительским epic и label `ERP_LABEL_EPIC_PLAN`.
10. Если child plan-epic уже существует, обнови его описание и используй его как canonical plan-epic для текущего запуска.
11. Если child plan-epic ещё не существует, создай его под родительским epic и обязательно добавь label `ERP_LABEL_EPIC_PLAN`.
12. Если canonical child plan-epic уже существовал, обнови его, а не создавай новый дубликат.
13. После успешного прохождения completion gates добавь комментарий о готовности плана к проверке на canonical child plan-epic. Не устанавливай отдельные plan-specific lifecycle labels и не ставь `ERP_LABEL_APPROVED` автоматически; принятие плана к декомпозиции фиксируется отдельной approval/review-процедурой через обычный `ERP_LABEL_APPROVED` на дочернем plan-epic.
14. Не предлагай пользователю альтернативные варианты сохранения плана вне ERP.

## Формат результата

```md
✅ План готов: <epic_name>
Эпик: <epic_link>
План: <plan_epic_link>
```

```md
❌ План не подготовлен: <epic_name>
Эпик: <epic_link>
reason: <reason>
```

Если URL эпика определить не удалось, строку `Эпик:` можно опустить.

Если во входе есть `epicUrl`, строку `Эпик:` заполняй этим значением.

Запрещено выводить:
- полный текст плана;
- длинные пояснения;
- внутренние рассуждения;
- служебные поля вроде `run status`, `lifecycle transition`, `gate marker`, `comment`.

## Ограничения

- Не использовать текст родительского epic как замену child plan-epic после того, как canonical plan-epic уже создан.
- Не начинать анализ текущей реализации до проверки, что локальные репозитории доступны и определены релевантные ориентиры по коду.
- Поиск текущей реализации обязателен для каждого запуска.
- Отсутствие найденной реализации не считать автоматически риском.
- Не создавать план вне ERP и не использовать локальный файл как source of truth для плана.
- Для смены gate/status scoped label на epic использовать только `AddLabel`, без полного reread/merge списка labels.
- Всегда переиспользовать существующий canonical child plan-epic, если он уже есть; не создавать дубликаты plan-epic для одного родительского epic.
- Отвечать в том же чате, где получен запрос.

## Смоук-чек

- Вход: валидный `epicId` с expected gate `ERP_LABEL_APPROVED`, уже существующим child plan-epic с label `ERP_LABEL_EPIC_PLAN`, обновлённым без создания дубликата и комментарием о готовности плана к проверке → ожидается `✅ План готов`.
- Вход: epic без expected gate marker `ERP_LABEL_APPROVED` → ожидается `❌ failed`, `reason code = epic_not_approved`.
- Вход: epic без достаточного `requirement-source` или с открытым критичным конфликтом с базой знаний → ожидается `❌ failed` на этапе readiness to planning.
- Вход: план создан, но комментарий со ссылкой на план не добавился → ожидается `❌ failed`, `reason code = epic_comment_failed`.
- Вход: план строится для новой функциональности и реализация не найдена → ожидается success при фиксации `existing implementation: not found`.
- Вход: релевантную реализацию не удалось уверенно идентифицировать → ожидается success или fail по контексту, но результат поиска должен быть зафиксирован как `existing implementation: not identified`.

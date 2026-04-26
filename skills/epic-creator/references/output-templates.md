# Output templates

Используй эти шаблоны как канонические формы ответа для `epic-creator`.

## Template A — epic not ready

```md
Не хватает данных, чтобы собрать epic для создания.

Название epic:
<canonical_title_if_available>

Краткое описание epic:
<short_summary_if_available>

Уточните, пожалуйста:
- <human_readable_label_1>: <what_user_should_provide>
- <human_readable_label_2>: <what_user_should_provide>

После этого я соберу финальную заготовку для создания epic.

Служебно: not_ready, reason: <common_reason_code> (`<placeholder-name-1>`, `<placeholder-name-2>`)
```

Если `Detail` нужен для диагностики, добавь его в служебную строку:

```md
Служебно: not_ready, reason: <common_reason_code>, detail: <local_detail_reason> (`<placeholder-name-1>`)
```

## Template B — ready to create

```md
✅ Данные для создания epic готовы.

Название epic:
<canonical_title>

Краткое описание epic:
<short_summary>

Что дальше: доработать описание, очистить текст от воды или создать epic в ERP?
```

## Template C — epic created

```md
✅ Epic создан: <epic_link>
```

## Rules

- `Detail` использовать только при необходимости точной диагностики; он не заменяет common reason code.
- В business-intake сценариях не начинай ответ с `Status`, `Reason`, `Missing`; сначала дай понятный итог и запрос действия.
- В служебной строке явно указывай outcome `not_ready` и используй только common reason code из `../../../docs/epic-reason-codes.md`.
- Человекочитаемые названия полей бери из `../../../docs/epic-template-dictionary.yaml`.
- В служебной строке перечисляй только канонические placeholder names.
- Если `Название epic` или `Краткое описание epic` ещё не сформированы, опускай соответствующую секцию целиком, а не выводи пустой заголовок.
- В запросе действия не проси пользователя переписывать весь epic, если не хватает только части placeholder names.
- Если `author` заполнен автоматически из sender metadata, не акцентируй это в финальном output без необходимости.
- Перед create-stage всегда выводи `Название epic` и `Краткое описание epic`.
- Если title не прошёл naming-check по `../../../docs/epic-naming.md`, используй `naming_not_stable` в служебной строке и не выполняй create-stage.
- Для runtime/config/preflight failures, не связанных с business-intake, технический `Status: ❌ failed` можно оставить в начале.
- До подтверждения пользователя не имитируй ERP result.
- Не выводи полный текст описания в чат; возвращай только ERP-ссылку после создания.

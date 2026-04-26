# Output templates

Используй эти шаблоны как канонические формы ответа для `epic-creator`.

## Template A — epic not ready

```md
Status: ❌ failed
Reason: <common_reason_code>
Detail: <local_detail_reason_if_needed>
Missing:
- <placeholder-name-1>
- <placeholder-name-2>

Why it matters:
<short explanation why these gaps block progress>

Next step:
Нужно прислать `<placeholder-name-1>` и `<placeholder-name-2>`.
```

## Template B — ready to create

```md
✅ Данные для создания epic готовы.

Название epic:
<canonical_title>

Краткое описание epic:
<short_summary>

Создать epic в ERP?
```

## Template C — epic created

```md
✅ Epic создан: <epic_link>
```

## Rules

- В `Reason` используй только common reason code из `../../../docs/epic-reason-codes.md`.
- `Detail` использовать только при необходимости точной диагностики; он не заменяет `Reason`.
- В `Missing` перечисляй только канонические placeholder names.
- В `Next step` не проси пользователя переписывать весь epic, если не хватает только части placeholder names.
- Если `author` заполнен автоматически из sender metadata, не акцентируй это в финальном output без необходимости.
- Перед create-stage всегда выводи `Название epic` и `Краткое описание epic`.
- Если title не прошёл naming-check по `../../../docs/epic-naming.md`, используй `Reason: naming_not_stable` и не выполняй create-stage.
- До подтверждения пользователя не имитируй ERP result.
- Не выводи полный текст описания в чат; возвращай только ERP-ссылку после создания.

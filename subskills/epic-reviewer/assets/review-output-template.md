# Review output template

Используй этот шаблон как канонический формат результата review.

## Full template

```md
Run Status: <in_progress | done | failed>
Готовность: <APPROVED | TO DEFINE | not_evaluated>
Reason: <reason_code | none>
Автор эпика: <AuthorFullName>
Критические блокеры: <number>
Разделов с замечаниями: <number>

Сводка по BABOK-блокам:
- Business requirements: <OK | GAP | RISK | CONFLICT>
- Stakeholder requirements: <OK | GAP | RISK | CONFLICT>
- Solution requirements / Functional: <OK | GAP | RISK | CONFLICT>
- Solution requirements / Non-functional: <OK | GAP | RISK | CONFLICT | N/A>
- Transition requirements: <OK | GAP | RISK | CONFLICT | N/A>
- Business rules: <OK | GAP | RISK | CONFLICT | N/A>
- Assumptions / Constraints / Dependencies: <OK | GAP | RISK | CONFLICT | N/A>

Integration Check:
- Case: <yes | no>
- Spec Status: <ok | missing | incomplete | conflict | n/a>
- Implementation Alignment: <ok | not_checked | conflict | n/a>

Duplicate Check:
- Status: <exact_duplicate | strong_overlap | partial_overlap | related_only | no_overlap>
- Findings:
  - <entity> — <link>
    - match: <type>
    - reason: <short explanation>
- Recommendation: <merge | narrow_scope | add_links | keep_independent | return_to_define>

Замечания:
- <Раздел 1>
  - Тип: <GAP | RISK | CONFLICT>
  - Критичность: <CRITICAL | NON_CRITICAL>
  - Проблема: <что не так>
  - Нужно уточнить: <что именно требуется>
  - Подтверждение: <цитата или фрагмент эпика>
- <Раздел 2>
  - Тип: <GAP | RISK | CONFLICT>
  - Критичность: <CRITICAL | NON_CRITICAL>
  - Проблема: <что не так>
  - Нужно уточнить: <что именно требуется>
  - Подтверждение: <цитата или фрагмент эпика>

Что нужно закрыть для APPROVED:
- <условие 1>
- <условие 2>
- <условие 3>
```

Если замечаний нет, явно пиши:

```md
Пробелы, противоречия и критические риски не выявлены.
```

## Compact template

Используй по умолчанию для ответа в чат. Для ERP-комментария compact template не использовать. Структуру сохраняй.

```md
Готовность: <APPROVED | TO DEFINE | not_evaluated>
Автор эпика: <AuthorFullName>
Ссылка: <epic_url>
Критические блокеры: <number>
Разделов с замечаниями: <number>

Сводка по BABOK-блокам:
- Business requirements: <status>
- Stakeholder requirements: <status>
- Functional: <status>
- Non-functional: <status>
- Transition: <status>
- Business rules: <status>
- Assumptions / Constraints / Dependencies: <status>

Integration Check:
- Case: <yes | no>
- Spec Status: <ok | missing | incomplete | conflict | n/a>
- Implementation Alignment: <ok | not_checked | conflict | n/a>

Duplicate Check:
- Status: <exact_duplicate | strong_overlap | partial_overlap | related_only | no_overlap>
- Findings:
  - <entity> — <link>: <short explanation>
- Recommendation: <merge | narrow_scope | add_links | keep_independent | return_to_define>

Ключевые замечания:
- <краткое замечание 1>
- <краткое замечание 2>

Что нужно закрыть для APPROVED:
- <условие 1>
- <условие 2>
```

## Rules

- `Run Status` обязательно различает технический статус review workflow и бизнес-вердикт по эпику.
- В поле `Готовность` используй только display-значения: `APPROVED`, `TO DEFINE`, `not_evaluated`.
- Никогда не выводи в `Готовность` lifecycle enum'ы `approved` или `to-define`.
- При `Run Status: failed` использовать `Готовность: not_evaluated`.
- `Reason` = конкретный code только при preflight failure, guardrail stop или явной подмене требований реализацией.
- Во всех остальных случаях `Reason: none`.
- В compact template для чата не выводи поля `Run Status` и `Reason`.
- Не меняй названия секций.
- Не добавляй перед шаблоном или между секциями operational-progress текст.
- Не убирай секцию `Что нужно закрыть для APPROVED`, даже если замечаний мало.

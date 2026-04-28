# Intake step templates

Используй эти шаблоны как message patterns для intake-мастера. Не копируй механически, но сохраняй структуру, краткость и привязку к placeholder names.

Если по ходу intake нужно объяснить, почему нельзя идти дальше, сначала дай человекочитаемый итог, а `not_ready`, common reason code из `../../../docs/epic-reason-codes.md` и локальный detail из SKILL.md вынеси в короткую служебную строку.

Человекочитаемые названия placeholder names бери из `../../../docs/epic-template-dictionary.yaml`.

## Template 1 — base intake

Использовать, когда нужно собрать minimum для осмысленного create-flow.

Не дублировать поля отдельным prose-блоком перед шаблоном: давать один компактный copy-ready шаблон для заполнения.
Сам шаблон всегда выводить fenced-блоком `text`.

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

## Template 2 — focused follow-up

Использовать, когда не хватает 1-3 placeholder names.

```md
Не хватает ещё нескольких данных.

Уточните, пожалуйста:
- <human_readable_label_1>: <what_user_should_provide>
- <human_readable_label_2>: <what_user_should_provide>
- <human_readable_label_3>: <what_user_should_provide>

Пришли только их, без переписывания всего эпика.

Служебно: not_ready, reason: missing_input (`<placeholder-1>`, `<placeholder-2>`, `<placeholder-3>`)
```

## Template 3 — supporting detail

Использовать после закрытия minimum для create-flow, когда нужно уточнить содержательные детали.

```md
Чтобы описание было осмысленным, уточни, пожалуйста:
- ожидаемый эффект;
- нужен ли AS-IS;
- есть ли важные правила и ограничения;
- есть ли UI-изменения;
- есть ли уже известные зависимости;
- есть ли ограничения;
- есть ли риски и допущения;
- есть ли ссылки на материалы.
```

## Template 4 — author clarification

Использовать только если `author` нельзя надёжно взять из sender metadata.

```md
Не могу надёжно определить `author` из sender metadata.
Напиши, пожалуйста, кто автор эпика: имя или identifier, который нужно подставить в `author`.
```

## Template 5 — requirement source blocker

Использовать, когда отсутствует обязательный `requirement-source`.

```md
Без источника требования нельзя понять основание эпика и проверить, что именно нужно реализовать.

Пришли источник требования: ТЗ, ЧТЗ, встреча, договорённость с ЛПР или другое основание.

Служебно: not_ready, reason: source_not_provided (`requirement-source`)
```

## Template 6 — codebase-check blocker

Использовать, когда для изменения существующей реализации или спорной delta нужен codebase-check, а без него нельзя надёжно собрать осмысленное описание для create-flow.

```md
Без проверки текущей реализации нельзя надёжно описать `as-is`, delta и зависимости.

Либо выполни codebase-check, либо пришли подтверждённые данные по текущему состоянию и границам изменения.

Служебно: not_ready, reason: insufficient_input_for_create, detail: codebase_check_required
```

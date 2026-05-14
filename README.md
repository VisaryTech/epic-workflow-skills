# Epic Workflow Skills

Пакет skills для работы с жизненным циклом эпиков: создание, очистка, review, доработка, подготовка плана реализации, декомпозиция в dev-задачи и оценка веса задач.

## Структура

```text
.
|-- SKILL.md                         # главный skill: маршрутизация и общие правила пакета
|-- agents/
|   `-- openai.yaml                  # настройки агента для пакета
|-- config/
|   `-- erp-env.json.example         # пример пользовательской ERP-конфигурации
|-- docs/                            # общая доменная база epic workflow
|   |-- epic-workflow.md             # человекочитаемые правила процесса
|   |-- epic-lifecycle.yaml          # machine-readable lifecycle и ERP label mapping
|   |-- epic-template.md             # шаблон описания эпика
|   |-- epic-template-dictionary.yaml # словарь полей шаблона
|   |-- epic-required-fields.md       # обязательные поля и проверки заполненности
|   |-- epic-quality-gates.md         # gates качества для переходов lifecycle
|   |-- epic-readiness-preflight.md   # preflight перед review/readiness
|   |-- epic-reason-codes.md          # канонические reason codes
|   |-- epic-writing-style.md         # правила стиля и формулировок
|   |-- epic-naming.md                # правила именования
|   `-- epic-glossary.md             # глоссарий терминов
|-- references/
|   `-- skill-map.md                 # краткая карта дочерних skills
|-- scripts/
|   |-- erp_config.py                # загрузка и валидация ERP-конфига
|   |-- get_erp_envs.py              # диагностика доступных ERP env values
|   |-- build_erp_url.py             # построение canonical ERP URL
|   `-- load_epic_lifecycle.py       # загрузка docs/epic-lifecycle.yaml
|-- subskills/                       # дочерние skills, выполняющие конкретные операции
|   |-- epic-creator/                # intake и создание нового epic в ERP
|   |-- epic-deduplicator/           # очистка текста epic от дублей и шума
|   |-- epic-reviewer/               # review готовности и lifecycle decision
|   |-- epic-refiner/                # доработка epic после замечаний
|   |-- epic-dev-plan-creator/       # создание или обновление implementation plan
|   |-- epic-task-creator/           # декомпозиция plan-epic в dev-задачи
|   `-- epic-task-weight-estimator/  # оценка веса задач, связанных с epic
`-- tests/
    `-- test_scripts.py
```

## Runtime dependencies

- Для ERP TaskTracker read/write операций должен быть установлен [visary-cloud-api-skills](https://github.com/VisaryTech/visary-cloud-api-skills).

## Конфигурация

### 1. Создать пользовательский ERP-конфиг

Скопируйте пример:

```powershell
New-Item -ItemType Directory -Force ~/.config
Copy-Item config/erp-env.json.example ~/.config/erp-env.json
```

Заполните реальные значения в `~/.config/erp-env.json`:

```json
{
  "ERP_BASE_URL": "https://erp.example.com",
  "ERP_PROJECT_ID": "123",
  "ERP_LABEL_EPIC_PLAN": "1801",
  "ERP_LABEL_DRAFT": "1792",
  "ERP_LABEL_TO_APPROVE": "1762",
  "ERP_LABEL_TO_DEFINE": "1785",
  "ERP_LABEL_APPROVED": "1763",
  "ERP_LABEL_READY": "1765"
}
```

### 2. Источник списка ERP label keys

Список обязательных `ERP_LABEL_*` не хранится вручную в скриптах. Он вычисляется из [`docs/epic-lifecycle.yaml`](docs/epic-lifecycle.yaml):

- `plan_epic_label_env` задает label для child epic с implementation plan.
- `status_env_map` задает label env key для каждого lifecycle status.

Если в lifecycle добавляется новый статус, нужно обновить `docs/epic-lifecycle.yaml`, затем добавить соответствующее значение в `~/.config/erp-env.json`.

### 3. Приоритет источников конфигурации

Скрипты читают значения в таком порядке:

1. Переменные окружения.
2. Пользовательский файл `~/.config/erp-env.json`.

Это позволяет временно переопределять значения без изменения пользовательского конфига.

Пример:

```powershell
$env:ERP_BASE_URL = "https://erp.local"
python scripts/get_erp_envs.py
```

### 4. Проверить конфигурацию

```powershell
python scripts/get_erp_envs.py
```

Команда выводит JSON с:

- `ok` - удалось ли загрузить конфигурацию;
- `config_path` - путь к пользовательскому конфигу;
- `config_example_path` - путь к примеру;
- `items` - найденные значения и источник каждого значения;
- `missing` - список отсутствующих обязательных ключей.

## Тесты

Запуск unit-тестов:

```powershell
python -m unittest discover tests
```

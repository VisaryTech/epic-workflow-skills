# Epic Workflow Skills

Пакет skills для работы с жизненным циклом эпиков: создание, очистка, review, доработка, подготовка плана реализации, декомпозиция в dev-задачи и оценка веса задач.

Главная точка входа - [`SKILL.md`](SKILL.md). Она маршрутизирует запросы в специализированные дочерние skills из [`skills/`](skills).

## Структура

```text
.
|-- SKILL.md                         # umbrella-skill и правила маршрутизации
|-- agents/
|   `-- openai.yaml                  # настройки агента для пакета
|-- config/
|   `-- erp-env.json.example         # пример пользовательской ERP-конфигурации
|-- docs/                            # общая доменная база epic workflow
|   |-- epic-workflow.md             # человекочитаемые правила процесса
|   |-- epic-lifecycle.yaml          # machine-readable lifecycle и ERP label mapping
|   |-- epic-template.md             # шаблон описания эпика
|   |-- epic-template-dictionary.yaml
|   |-- epic-required-fields.md
|   |-- epic-quality-gates.md
|   |-- epic-readiness-preflight.md
|   |-- epic-reason-codes.md
|   |-- epic-writing-style.md
|   |-- epic-naming.md
|   `-- epic-glossary.md
|-- references/
|   `-- skill-map.md                 # краткая карта дочерних skills
|-- scripts/
|   |-- erp_config.py                # загрузка и валидация ERP-конфига
|   |-- get_erp_envs.py              # диагностика доступных ERP env values
|   |-- build_erp_url.py             # построение canonical ERP URL
|   `-- load_epic_lifecycle.py       # загрузка docs/epic-lifecycle.yaml
|-- skills/
|   |-- epic-creator/
|   |-- epic-deduplicator/
|   |-- epic-reviewer/
|   |-- epic-refiner/
|   |-- epic-dev-plan-creator/
|   |-- epic-task-creator/
|   `-- epic-task-weight-estimator/
`-- tests/
    `-- test_scripts.py
```

### Роли основных директорий

- `docs/` - общий источник правил, терминов, lifecycle, шаблонов и quality gates. Дочерние skills должны ссылаться на эти документы, а не дублировать общие правила.
- `skills/` - исполняемый capability-слой. Каждый подкаталог содержит отдельный `SKILL.md` и, при необходимости, свои `references/`, `assets/` или `agents/`.
- `scripts/` - вспомогательные Python-скрипты для конфигурации и построения ERP-ссылок.
- `config/` - пример пользовательской ERP-конфигурации. Реальный `erp-env.json` хранится вне репозитория.
- `references/` - короткие навигационные материалы по пакету.

## Runtime dependencies

- Для ERP TaskTracker read/write операций должен быть установлен `visary-cloud-api-skills`.
- Этот пакет использует TaskTracker API capability внутри `visary-cloud-api-skills`.
- Локальные скрипты этого репозитория не вызывают внутренние API CLI-скрипты `visary-cloud-api-skills` напрямую.
- ERP-конфиг хранится отдельно в `~/.config/erp-env.json`.

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

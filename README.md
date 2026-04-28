# Epic Workflow Skills

Пакет skills для работы с жизненным циклом эпиков: создание, очистка, review, доработка, подготовка плана реализации, декомпозиция в dev-задачи и оценка веса задач.

Главная точка входа - [`SKILL.md`](SKILL.md). Она маршрутизирует запросы в специализированные дочерние skills из [`subskills/`](subskills).

## Структура

Репозиторий устроен как пакет skills с одним главным skill и набором специализированных дочерних skills. Верхний [`SKILL.md`](SKILL.md) отвечает за маршрутизацию намерения пользователя, а директории `docs/`, `scripts/` и `subskills/` задают общую доменную базу, технические утилиты и исполняемые capability-модули.

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

### Роли основных директорий

- `SKILL.md` - верхнеуровневый entrypoint пакета. Он не реализует все сценарии сам, а выбирает нужный дочерний skill по intent пользователя.
- `docs/` - общий источник правил, терминов, lifecycle, шаблонов и quality gates. Дочерние skills должны ссылаться на эти документы, а не дублировать общие правила.
- `subskills/` - исполняемый capability-слой. Каждый подкаталог содержит отдельный `SKILL.md` со своим контрактом входных данных, preflight, процессом, форматом результата и ограничениями. Если skill нужны локальные примеры, шаблоны или настройки агента, они лежат внутри этого же подкаталога в `references/`, `assets/` или `agents/`.
- `scripts/` - вспомогательные Python-скрипты для конфигурации и построения ERP-ссылок.
- `config/` - пример пользовательской ERP-конфигурации. Реальный `erp-env.json` хранится вне репозитория.
- `references/` - короткие навигационные материалы по пакету, в первую очередь карта дочерних skills и их scope.
- `tests/` - unit-тесты для локальных скриптов и правил загрузки конфигурации/lifecycle.

### Дочерние skills

- `subskills/epic-creator` - собирает intake, проверяет обязательные поля и создает новый epic в ERP.
- `subskills/epic-deduplicator` - убирает повторы, лишние формулировки и шум без изменения бизнес-смысла epic.
- `subskills/epic-reviewer` - проверяет готовность epic и возвращает lifecycle decision `approved` или `to-define`.
- `subskills/epic-refiner` - дорабатывает epic по замечаниям review, особенно для возврата из `to-define`.
- `subskills/epic-dev-plan-creator` - готовит implementation plan как дочерний plan-epic с label `ERP_LABEL_EPIC_PLAN`.
- `subskills/epic-task-creator` - декомпозирует approved child plan-epic в ERP dev-задачи с проверкой по текущей кодовой базе.
- `subskills/epic-task-weight-estimator` - оценивает вес задач, связанных с epic.

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

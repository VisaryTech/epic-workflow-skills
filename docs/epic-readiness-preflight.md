# Epic readiness preflight

Общий preflight-baseline перед созданием epic в ERP и запуском formal review.

## Scope

Этот документ определяет:
- минимальный screening перед `create` и `formal review`;
- блокирующие входные gaps;
- исходы `not_ready | ready_for_create | ready_for_review`;
- стратегию уточняющих вопросов.

## Not in scope

Этот документ не определяет:
- lifecycle и transition rules, для этого использовать `docs/epic-workflow.md` и `docs/epic-lifecycle.yaml`;
- stage-specific placeholder requirements, для этого использовать `docs/epic-required-fields.md`;
- полный quality review и formal verdict, для этого использовать `docs/epic-quality-gates.md` и review checklist;
- operational behavior skills при reread, mismatch, sync и hidden entities, для этого использовать `docs/epic-skill-baseline.md`.

Это screening-слой, а не formal review. Он отвечает только на вопросы:
- есть ли минимально достаточная основа, чтобы продолжать create/review flow;
- какие блоки данных нужно добрать до следующего шага;
- какие gaps являются блокирующими уже на входе.

## Purpose

Перед созданием epic в ERP или запуском formal review:
- проверить, что собраны критичные requirement-блоки;
- не пропустить очевидные blockers на входе;
- сформировать пакет уточняющих вопросов по недостающим данным.

## Preflight outcomes

Используй три исхода.

### 1. `not_ready`
Применять, если отсутствует хотя бы один критичный входной блок и без него нельзя осмысленно продолжать create/review flow.

### 2. `ready_for_create`
Применять, если данных достаточно для осмысленного создания epic, но недостаточно для запуска уверенного formal review.

### 3. `ready_for_review`
Применять, если входные блоки собраны на уровне, достаточном для formal review.

## Critical entry blocks

### 1. Business basis
Нужно подтвердить:
- `business-goal`;
- `problem`;
- `expected-effect`, если уже заявлен переход к review.

Блокирует вход дальше, если непонятно, зачем изменение нужно бизнесу и какой результат ожидается.

### 2. Ownership and actors
Нужно подтвердить:
- кто инициатор или владелец области;
- кто принимает решение;
- какие роли или пользователи получают ценность.

Блокирует вход дальше, если непонятно, для кого и в чьей зоне ответственности описывается изменение.

### 3. Change scope
Нужно подтвердить:
- что именно меняется;
- в какой подсистеме / модуле;
- где проходит граница `scope`;
- когда это важно, что находится в `out-of-scope`.

Блокирует вход дальше, если объект изменения и границы работ не отделимы от соседних инициатив.

### 4. Functional basis
Нужно подтвердить:
- целевую логику на уровне `to-be-logic`;
- хотя бы один ключевой сценарий;
- если это change existing behavior, текущий контекст (`as-is`) там, где без него непонятна delta.

Блокирует вход дальше, если требования сведены к общей идее без наблюдаемого поведения системы.

### 5. Acceptance basis
Нужно подтвердить:
- есть ли проверяемый каркас `acceptance-criteria`;
- можно ли по ним понять ожидаемый результат.

Для create-flow допустима неполная проработка AC, если уже есть проверяемый каркас.
Для review отсутствие проверяемых AC является блокером.

### 6. Source traceability
Нужно подтвердить:
- есть ли `requirement-source`;
- есть ли `additional-materials`, если на них опирается формулировка.

Отсутствие источника требования является блокером.

### 7. Data / integration / process impact
Подтверждать только если релевантно:
- затрагиваемые данные, сущности, статусы, формы;
- интеграции и внешние системы;
- process/workflow impact.

Если влияние заявлено, но не определено на базовом уровне, это блокер для review и может быть блокером для create-flow по контексту.

### 8. Constraints / dependencies / risks
Нужно подтвердить только то, что уже влияет на оценку и понимание объёма:
- ограничения;
- зависимости;
- существенные риски и допущения.

Если без этих факторов невозможно безопасно понимать объём работ, это блокер.

## Integration-case preflight

Считать epic integration-case, если он описывает:
- межсистемный обмен;
- API;
- webhook;
- event / queue;
- file exchange;
- доработку существующей интеграции.

Для integration-case на preflight нужно подтвердить:
- наличие проверяемой спецификации интеграции в `requirement-source` и/или `additional-materials`;
- понятность контракта обмена, состава данных и направления интеграции.

Если integration-case заявлен, но проверяемой спецификации нет, исход не выше `ready_for_create`; для formal review это блокер.

## Codebase-check policy

Используй codebase-check как входную валидацию только когда он действительно нужен.

Codebase-check обязателен, если:
- epic описывает изменение существующей реализации;
- меняется существующий модуль, экран, процесс или интеграция;
- без текущего состояния нельзя надёжно описать `as-is` или delta;
- без codebase-check create-flow или review будет опираться на догадки.

Если codebase-check обязателен, но недоступен:
- не выдумывай `as-is`, зависимости и текущую реализацию;
- используй `Reason: insufficient_input_for_create` или аналогичный blocking outcome текущего flow;
- при необходимости добавляй `Detail: codebase_check_required`.

## Minimal interpretation rules

- `not_ready` — нет минимально достаточной базы даже для осмысленного создания epic или входа в review.
- `ready_for_create` — можно создавать epic, но нельзя автоматически считать его готовым к formal review.
- `ready_for_review` — можно запускать formal review, но это не гарантирует итоговый verdict `APPROVED`.

## Question strategy

Задавай вопросы пакетами по 2-4 связанных пункта:
- сначала business basis + ownership;
- затем change scope + key scenario;
- затем acceptance basis + constraints/dependencies;
- затем только контекстные ветки: UI, data, integrations, transition.

Не превращай preflight в полный review checklist.

## Guardrails

- Не выполнять formal verdict `APPROVED / TO DEFINE` внутри preflight.
- Не дублировать deep review checklist.
- Не маскировать отсутствие требований красивым prose.
- Если найден blocker, сначала добрать данные, а не симулировать полноту.
- Если epic проходит только как `ready_for_create`, не называть его готовым к review автоматически.

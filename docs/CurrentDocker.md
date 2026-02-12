# Current Docker Setup - BADK Official

**Сервер**: `192.168.0.230` (ssh alias: `badk`, пользователь: `webadmin`)  
**Проект**: `/var/www/badk-official/`  
**Дата анализа**: 12 февраля 2026

---

## Архитектура (что сейчас стоит)

```
Internet → nginx (reverse proxy) → Docker Container (badk_official) → Django runserver :8000
                                   ├─ PostgreSQL :5432 (badk-db)
                                   └─ Redis :6379 (badk-redis)
```

**3 сервиса в docker-compose.yml:**

### 1. badk_official (Django app)
- **Image**: custom build (`Dockerfile` с Python 3.12)
- **Command**: `.venv/bin/python manage.py runserver 0.0.0.0:8000`
- **Port**: `8000:8000`
- **Volume**: `./:/var/www/project` — **bind-mount проекта с хоста**
- **Restart**: `always`

### 2. postgres (база данных)
- **Image**: `postgres:14.6-alpine`
- **Container**: `badk-db`
- **Port**: `5432:5432`
- **Volume**: `../badk-db-data:/var/lib/postgresql/data/`
- **Env**: из `.env` файла (USER/PASSWORD/DB)

### 3. redis (кэш + celery broker)
- **Image**: `redis:7.0-alpine`
- **Container**: `badk-redis`
- **Restart**: `always`

---

## Dockerfile (build образа)

```dockerfile
FROM python:3.12
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN pip install --upgrade pip && pip install poetry

COPY poetry.lock pyproject.toml /var/www/project/
WORKDIR /var/www/project

RUN poetry config virtualenvs.in-project true \
    && poetry install --no-root

COPY . /var/www/project
EXPOSE 8000
```

**Что делает:**
1. Копирует `poetry.lock` + `pyproject.toml`
2. Создаёт `.venv` внутри проекта (`virtualenvs.in-project`)
3. Устанавливает зависимости через `poetry install --no-root`
4. Копирует весь проект
5. Открывает порт 8000

---

## Проблемы текущего setup'а

### 🔴 КРИТИЧЕСКАЯ: Bind-mount конфликт
**Что происходит:**
- В `Dockerfile` ставятся зависимости → создаётся `.venv/` в образе
- **НО** при старте контейнера монтируется `./:/var/www/project`
- Если на хосте `.venv/` создан с другой версией Python (3.10) или вообще нет — **Django не находится**
- **Результат**: `ModuleNotFoundError: No module named 'django'`, контейнер рестартится бесконечно

**Почему так сделано:**
- Для разработки удобно: меняешь код локально → сразу видно в контейнере
- Но для продакшена это **анти-паттерн** — код должен быть **в образе**, а не на хосте

### 🟡 Development server в проде
**Сейчас:**
```bash
command: sh -c ".venv/bin/python manage.py runserver 0.0.0.0:8000"
```

**Проблема:**
- `runserver` — это **dev-сервер Django**, не для продакшена
- **Не умеет**: многопоточность, обработку нагрузки, graceful shutdown
- **Должно быть**: `gunicorn` или `uvicorn` (асинхронный)

**Результат:**
- При любом крэше Python процесса → nginx возвращает `502 Bad Gateway`
- Нет мониторинга, нет graceful restart

### 🟡 Poetry в runtime
**Старый подход (был раньше):**
```bash
poetry run python manage.py runserver
```

**Проблема:**
- Poetry дёргает свой кэш virtualenv'ов (обычно в `~/.cache/pypoetry`)
- В контейнере этого кэша нет → падает

**Текущий фикс:**
- Прямой запуск `.venv/bin/python`
- Но это костыль, не решает bind-mount конфликт

### 🟢 Хорошие моменты
- PostgreSQL и Redis в отдельных контейнерах — правильно
- `restart: always` — автоматический перезапуск при крэше
- `.env` файл для секретов — безопасно
- Volume для БД (`badk-db-data`) — данные не теряются

---

## Как это должно работать (best practice)

### Вариант А: Полноценный Docker для прода
```yaml
services:
  badk_official:
    build: .
    # БЕЗ bind-mount! Код в образе
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
    restart: always
    depends_on:
      - postgres
      - redis
```

**Изменения:**
1. Убрать `volumes: ./:/var/www/project`
2. Заменить `runserver` → `gunicorn`
3. При деплое: `docker compose build && docker compose up -d`

**Плюсы:**
- Гарантированно работает (всё в образе)
- Правильный WSGI сервер

**Минусы:**
- Каждый деплой = rebuild образа (1-2 минуты)

### Вариант Б: Systemd + gunicorn без Docker
```bash
# На хосте
cd /var/www/badk-official
.venv/bin/gunicorn config.wsgi:application --bind 127.0.0.1:8000 --workers 4 --daemon

# nginx проксирует на 127.0.0.1:8000
```

**Плюсы:**
- Нет Docker overhead
- Простой деплой: `git pull && systemctl restart gunicorn`

**Минусы:**
- Нужно настроить systemd unit
- Зависимости ставятся на хост (но у нас и так уже есть `.venv`)

---

## Текущий деплой (как делается сейчас)

```bash
ssh badk
cd /var/www/badk-official
git stash    # если есть локальные изменения
git pull
docker compose up -d --build badk_official
```

**Что происходит:**
1. Код обновляется на хосте
2. Контейнер перезапускается
3. **Проблема**: `.venv` на хосте может не соответствовать зависимостям в образе

---

## Рекомендации для фикса

### Срочно (чтобы работало прямо сейчас):
1. **На хосте создать `.venv` с Python 3.12:**
   ```bash
   python3.12 -m venv .venv
   .venv/bin/pip install poetry
   POETRY_VIRTUALENVS_IN_PROJECT=true .venv/bin/poetry install --no-root
   ```

2. **Проверить, что контейнер видит правильный `.venv`:**
   ```bash
   docker compose exec badk_official ls -la /var/www/project/.venv/bin/python
   ```

### Долгосрочно (архитектурно правильно):
1. **Вариант 1**: Убрать bind-mount, делать `docker compose build` при деплое
2. **Вариант 2**: Уйти от Docker, использовать systemd + gunicorn
3. Заменить `runserver` → `gunicorn` в любом случае
4. Добавить healthcheck в `docker-compose.yml`

---

## Команды для диагностики

```bash
# Статус контейнеров
docker ps -a

# Логи последние 100 строк
docker compose logs badk_official --tail=100

# Зайти внутрь контейнера
docker compose exec badk_official bash

# Проверить Python версию в контейнере
docker compose exec badk_official python --version

# Проверить, что Django доступен
docker compose exec badk_official python -c "import django; print(django.VERSION)"

# Перезапуск без rebuild
docker compose restart badk_official

# Полный rebuild
docker compose up -d --build badk_official
```

---

**Итог:** Setup работает, но находится в "костыльном" состоянии из-за смеси dev-практик (bind-mount, runserver) и prod-окружения (Docker Compose на боевом сервере). Надо либо зафиксить версии Python и собирать `.venv` правильно, либо переделать на production-ready архитектуру.

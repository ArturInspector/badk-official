## Деплой i18n (без preview)

1) Бэкап:
- `pg_dump $DB_NAME > pre-i18n.sql`

2) Подготовка окружения:
- `python -m venv .venv && . .venv/bin/activate`
- `pip install -r requirements.txt` (или `poetry install`)
- Экспортируй `DJANGO_SETTINGS_MODULE=config.settings` + обязательные переменные (`SECRET_KEY`, `ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, доступы к БД).

3) Синхронизация переводных полей (создаёт *_ru/_ky/_en в БД, если таблицы уже есть):
- `.venv/bin/python manage.py sync_translation_fields --noinput`

4) Миграции:
- `.venv/bin/python manage.py migrate`

5) Компиляция сообщений:
- `.venv/bin/python manage.py compilemessages`

6) Сборка статики (если требуется):
- `.venv/bin/python manage.py collectstatic --noinput`

7) Перезапуск сервисов:
- `docker compose down && docker compose up -d` (или `systemctl restart gunicorn && systemctl restart nginx`)

8) Smoke-тест:
- Переключатель языков RU/KY/EN сохраняет выбор и влияет на URL `/ky/...`, `/en/...`.
- Публичные страницы: главная, новости, специальности, сотрудничество, контакты — тексты локализуются.
- Админка: вкладки переводов в News/Specialty/Core/Employee/Student/Feedback.
- Фолбэк: при отсутствии перевода показывается RU.


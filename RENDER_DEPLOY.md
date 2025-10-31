# 🎨 Render - Пошаговая инструкция деплоя

## Шаг 1: Регистрация

1. Перейдите на https://render.com
2. Нажмите "Get Started for Free"
3. Войдите через GitHub
4. Подтвердите доступ к репозиториям

## Шаг 2: Создание Web Service

1. Нажмите "New +"
2. Выберите "Web Service"
3. Подключите репозиторий `vasilievyakov/tgcursor2`
4. Нажмите "Connect"

## Шаг 3: Настройка Web Service

Заполните форму:

- **Name:** `tgcursor2-backend`
- **Environment:** `Python 3`
- **Region:** выберите ближайший (например, Frankfurt)
- **Branch:** `main`
- **Root Directory:** `backend`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Шаг 4: Добавление PostgreSQL

1. Нажмите "New +"
2. Выберите "PostgreSQL"
3. Настройки:
   - **Name:** `tgcursor2-db`
   - **Database:** `tgcursor2` (или оставьте по умолчанию)
   - **User:** `tgcursor2_user` (или по умолчанию)
   - **Region:** тот же что и Web Service
   - **Plan:** Free (для начала)
4. Нажмите "Create Database"
5. Скопируйте **Internal Database URL** (для Web Service)

## Шаг 5: Добавление Redis

1. Нажмите "New +"
2. Выберите "Redis"
3. Настройки:
   - **Name:** `tgcursor2-redis`
   - **Region:** тот же что и Web Service
   - **Plan:** Free
4. Нажмите "Create Redis"
5. Скопируйте **Internal Redis URL** (для Web Service)

## Шаг 6: Настройка переменных окружения

1. Вернитесь в ваш Web Service
2. **Environment** → **Environment Variables**
3. Добавьте переменные:

```
DATABASE_URL=<Internal Database URL из PostgreSQL>
REDIS_URL=<Internal Redis URL из Redis>
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
SECRET_KEY=сгенерируйте_ключ_ниже
ENVIRONMENT=production
ALLOWED_ORIGINS=https://vasilievyakov.github.io,https://vasilievyakov.github.io/tgcursor2
```

**Генерация SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Шаг 7: Деплой

1. Нажмите "Create Web Service"
2. Render автоматически запустит деплой
3. Дождитесь завершения (обычно 3-5 минут)
4. После деплоя будет доступен URL типа: `https://tgcursor2-backend.onrender.com`

## Шаг 8: Выполнение миграций

1. Откройте **Shell** в вашем Web Service
2. Выполните:
```bash
alembic upgrade head
```

Или через Render Dashboard:
1. **Environment** → **Shell**
2. Выполните команду миграции

## Шаг 9: Обновление Frontend

1. Скопируйте URL вашего backend (например: `https://tgcursor2-backend.onrender.com`)
2. Обновите Secret в GitHub:
```bash
gh secret set VITE_API_URL --body "https://tgcursor2-backend.onrender.com" --repo vasilievyakov/tgcursor2
```

3. Перезапустите frontend workflow:
```bash
gh workflow run deploy-pages.yml --repo vasilievyakov/tgcursor2
```

## ✅ Готово!

Ваш backend будет доступен по адресу типа:
`https://your-service.onrender.com`

API документация:
`https://your-service.onrender.com/docs`

---

## ⚠️ Важные замечания:

1. **Сервис засыпает** после 15 минут бездействия (на бесплатном тарифе)
2. Первый запрос после пробуждения может занять 30-60 секунд
3. Для продакшн рассмотрите платный тариф ($7/месяц)

---

## 🔍 Полезные команды в Render Shell:

```bash
# Выполнить миграции
alembic upgrade head

# Проверить подключение к БД
python -c "from app.core.database import engine; print(engine)"

# Посмотреть логи
# Используйте вкладку "Logs" в Render Dashboard
```


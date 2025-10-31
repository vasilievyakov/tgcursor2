# 🚂 Railway - Пошаговая инструкция деплоя

## Шаг 1: Регистрация

1. Перейдите на https://railway.app
2. Нажмите "Start a New Project"
3. Войдите через GitHub
4. Подтвердите доступ к репозиториям

## Шаг 2: Создание проекта

1. Нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Найдите и выберите `vasilievyakov/tgcursor2`
4. Railway автоматически определит проект

## Шаг 3: Настройка проекта

1. **Нажмите на ваш проект** в Railway dashboard
2. **Settings** (в правом верхнем углу)
3. **Root Directory:** установите `backend`
4. Сохраните

## Шаг 4: Добавление PostgreSQL

1. В проекте нажмите **"New"**
2. Выберите **"Database" → "Add PostgreSQL"**
3. Railway автоматически создаст базу данных
4. Переменная `DATABASE_URL` будет добавлена автоматически

## Шаг 5: Добавление Redis

1. В проекте нажмите **"New"**
2. Выберите **"Database" → "Add Redis"**
3. Railway автоматически создаст Redis
4. Переменная `REDIS_URL` будет добавлена автоматически

## Шаг 6: Настройка переменных окружения

1. **Settings → Variables**
2. Нажмите **"New Variable"** и добавьте:

```
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

## Шаг 7: Настройка Start Command

1. **Settings → Deploy**
2. **Start Command:** установите:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Шаг 8: Выполнение миграций

1. После первого деплоя откройте **View Logs**
2. Или используйте Railway CLI:
```bash
# Установите Railway CLI
npm install -g @railway/cli

# Войдите
railway login

# Подключите проект
railway link

# Выполните миграции
railway run alembic upgrade head
```

## Шаг 9: Получение URL

1. После деплоя Railway автоматически создаст URL
2. Нажмите на сервис → **Settings → Domains**
3. Скопируйте URL (например: `https://tgcursor2-production.up.railway.app`)

## Шаг 10: Обновление Frontend

1. Обновите Secret в GitHub:
```bash
gh secret set VITE_API_URL --body "https://your-backend.railway.app" --repo vasilievyakov/tgcursor2
```

2. Перезапустите frontend workflow:
```bash
gh workflow run deploy-pages.yml --repo vasilievyakov/tgcursor2
```

## ✅ Готово!

Ваш backend будет доступен по адресу типа:
`https://your-project.railway.app`

API документация:
`https://your-project.railway.app/docs`

---

## 🔍 Полезные команды Railway CLI

```bash
# Посмотреть логи
railway logs

# Выполнить команду в контейнере
railway run <command>

# Открыть shell
railway shell

# Посмотреть переменные окружения
railway variables
```


# 🚀 Fly.io - Пошаговая инструкция деплоя

## Шаг 1: Установка Fly CLI

**Windows (PowerShell):**
```powershell
iwr https://fly.io/install.ps1 -useb | iex
```

**Или через winget:**
```powershell
winget install --id=Fly.Flyctl
```

**Linux/Mac:**
```bash
curl -L https://fly.io/install.sh | sh
```

## Шаг 2: Регистрация

1. Перейдите на https://fly.io
2. Зарегистрируйтесь (можно через GitHub)
3. Подтвердите email

## Шаг 3: Вход в CLI

```bash
fly auth login
```

Откроется браузер для авторизации.

## Шаг 4: Подготовка проекта

В директории `backend`:

```bash
cd backend
fly launch
```

Fly спросит:
- **App name:** `tgcursor2-backend` (или оставьте предложенное)
- **Region:** выберите ближайший (например, `fra` для Frankfurt)
- **PostgreSQL:** выберите "Yes" (Fly создаст для вас)
- **Redis:** выберите "Yes" (Fly создаст для вас)

## Шаг 5: Настройка fly.toml

Fly автоматически создаст `fly.toml`. Проверьте что:

```toml
[build]
  dockerfile = "Dockerfile"

[env]
  PORT = "8000"

[[services]]
  http_checks = []
  internal_port = 8000
  processes = ["app"]
  protocol = "tcp"
  script_checks = []
```

## Шаг 6: Настройка переменных окружения

```bash
fly secrets set TELEGRAM_API_ID=your_api_id_here
fly secrets set TELEGRAM_API_HASH=your_api_hash_here
fly secrets set SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(32))")
fly secrets set ENVIRONMENT=production
fly secrets set ALLOWED_ORIGINS=https://vasilievyakov.github.io,https://vasilievyakov.github.io/tgcursor2
```

**Или через файл:**
```bash
fly secrets set --file secrets.env
```

Где `secrets.env` содержит:
```
TELEGRAM_API_ID=your_api_id
TELEGRAM_API_HASH=your_api_hash
SECRET_KEY=сгенерированный_ключ
ENVIRONMENT=production
ALLOWED_ORIGINS=https://vasilievyakov.github.io,https://vasilievyakov.github.io/tgcursor2
```

## Шаг 7: Настройка PostgreSQL URL

Fly автоматически создаст PostgreSQL и добавит `DATABASE_URL`. Проверьте:

```bash
fly secrets list
```

Должна быть переменная `DATABASE_URL`.

## Шаг 8: Настройка Redis URL

Fly автоматически создаст Redis. Проверьте:

```bash
fly redis list
```

Получите URL:
```bash
fly redis status
```

Добавьте в секреты:
```bash
fly secrets set REDIS_URL=$(fly redis status --app your-redis-app-name | grep "Upstash Redis URL" | awk '{print $NF}')
```

## Шаг 9: Обновление Dockerfile (если нужно)

Убедитесь что `Dockerfile` использует переменную `PORT`:

```dockerfile
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "${PORT:-8000}"]
```

Или используйте переменную окружения:
```dockerfile
ENV PORT=8000
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Шаг 10: Деплой

```bash
fly deploy
```

Fly автоматически:
- Соберет Docker образ
- Задеплоит на серверы
- Настроит DNS
- Выдаст HTTPS сертификат

## Шаг 11: Выполнение миграций

После деплоя:

```bash
fly ssh console
```

Внутри контейнера:
```bash
alembic upgrade head
```

Или напрямую:
```bash
fly ssh console -C "alembic upgrade head"
```

## Шаг 12: Получение URL

```bash
fly status
```

Или проверьте в Dashboard: https://fly.io/dashboard

URL будет типа: `https://tgcursor2-backend.fly.dev`

## Шаг 13: Обновление Frontend

1. Скопируйте URL вашего backend
2. Обновите Secret в GitHub:
```bash
gh secret set VITE_API_URL --body "https://tgcursor2-backend.fly.dev" --repo vasilievyakov/tgcursor2
```

3. Перезапустите frontend workflow:
```bash
gh workflow run deploy-pages.yml --repo vasilievyakov/tgcursor2
```

## ✅ Готово!

Ваш backend будет доступен по адресу типа:
`https://your-app.fly.dev`

API документация:
`https://your-app.fly.dev/docs`

---

## 🔍 Полезные команды Fly.io:

```bash
# Посмотреть логи
fly logs

# Посмотреть статус
fly status

# Открыть shell
fly ssh console

# Посмотреть секреты
fly secrets list

# Перезапустить приложение
fly restart

# Посмотреть метрики
fly metrics
```

---

## 💡 Автоматический деплой из GitHub

1. В Fly Dashboard → Settings → GitHub Integration
2. Подключите репозиторий
3. Настройте:
   - **Root Directory:** `backend`
   - **Dockerfile Path:** `backend/Dockerfile`
4. При каждом push в `main` будет автоматический деплой


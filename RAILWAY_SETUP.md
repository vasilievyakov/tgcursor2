# Railway Деплой - Автоматическая настройка

## Переменные окружения для Railway:

```
TELEGRAM_API_ID=your_api_id_here
TELEGRAM_API_HASH=your_api_hash_here
SECRET_KEY=СГЕНЕРИРУЙТЕ_НОВЫЙ_КЛЮЧ
ENVIRONMENT=production
ALLOWED_ORIGINS=https://vasilievyakov.github.io,https://vasilievyakov.github.io/tgcursor2
```

## Start Command:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## Root Directory:
```
backend
```

## Миграции:
После деплоя выполните:
```bash
railway run alembic upgrade head
```

## После получения URL backend:
1. Обновите VITE_API_URL secret в GitHub:
   ```bash
   gh secret set VITE_API_URL --body "https://your-backend.railway.app" --repo vasilievyakov/tgcursor2
   ```

2. Перезапустите frontend workflow:
   ```bash
   gh workflow run deploy-pages.yml --repo vasilievyakov/tgcursor2
   ```


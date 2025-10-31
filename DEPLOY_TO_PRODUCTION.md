# Деплой проекта на GitHub и публичный доступ

## 📋 План действий

### 1. Подготовка к GitHub

#### Шаг 1: Проверка и коммит изменений

```bash
# Проверить статус
git status

# Добавить все файлы
git add .

# Создать коммит
git commit -m "feat: переделан дизайн на shadcn/ui, готов к деплою"

# Проверить текущую ветку
git branch
```

#### Шаг 2: Создание репозитория на GitHub

1. Перейдите на https://github.com/new
2. Создайте новый репозиторий (например, `tgcursor2`)
3. **НЕ** добавляйте README, .gitignore или лицензию (они уже есть)
4. Скопируйте URL репозитория

#### Шаг 3: Привязка к удаленному репозиторию

```bash
# Добавить remote (замените YOUR_USERNAME на ваш GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/tgcursor2.git

# Или через SSH
git remote add origin git@github.com:YOUR_USERNAME/tgcursor2.git

# Проверить remote
git remote -v

# Отправить код на GitHub
git push -u origin main
# или если ветка называется master:
git push -u origin master
```

---

## 🌐 Деплой в интернет

### Вариант 1: Vercel (Рекомендуется для Frontend + Backend)

**Плюсы:** Бесплатный, автоматический деплой из GitHub, SSL, CDN

#### Frontend на Vercel:

1. Перейдите на https://vercel.com
2. Войдите через GitHub
3. Нажмите "New Project"
4. Выберите репозиторий `tgcursor2`
5. Настройки:
   - **Root Directory:** `frontend`
   - **Framework Preset:** Vite
   - **Build Command:** `npm run build`
   - **Output Directory:** `dist`
   - **Install Command:** `npm install`

6. **Environment Variables:**
   ```
   VITE_API_URL=https://your-backend-url.vercel.app
   ```

7. Deploy!

#### Backend на Vercel:

1. Используйте существующий `vercel.json`
2. Настройте переменные окружения в Vercel dashboard
3. Deploy!

---

### Вариант 2: Railway (Backend) + Vercel (Frontend) ⭐ Рекомендуется

#### Backend на Railway:

1. Перейдите на https://railway.app
2. Войдите через GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Выберите репозиторий
5. Настройки:
   - **Root Directory:** `backend`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Build Command:** `pip install -r requirements.txt`

6. **Environment Variables:**
   ```
   DATABASE_URL=postgresql://... (Railway автоматически создаст)
   TELEGRAM_API_ID=your_id
   TELEGRAM_API_HASH=your_hash
   REDIS_URL=redis://... (Railway автоматически создаст)
   ALLOWED_ORIGINS=https://your-frontend.vercel.app
   SECRET_KEY=generate-strong-random-key
   ```

7. Railway автоматически создаст PostgreSQL и Redis

8. Выполните миграции:
   ```bash
   railway run alembic upgrade head
   ```

#### Frontend на Vercel:

1. См. вариант 1 выше
2. Используйте Railway URL для `VITE_API_URL`

---

### Вариант 3: Render (Backend + Frontend)

#### Backend на Render:

1. Перейдите на https://render.com
2. "New" → "Web Service"
3. Подключите GitHub репозиторий
4. Настройки:
   - **Name:** `tgcursor2-backend`
   - **Environment:** Python 3
   - **Build Command:** `cd backend && pip install -r requirements.txt`
   - **Start Command:** `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** `backend`

5. **Environment Variables:** (те же что выше)

#### Frontend на Render:

1. "New" → "Static Site"
2. Подключите репозиторий
3. Настройки:
   - **Root Directory:** `frontend`
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
   - **Environment:** `VITE_API_URL=https://your-backend.onrender.com`

---

## ⚙️ Настройка для продакшн

### 1. Обновите переменные окружения

**Frontend (.env.production или в Vercel):**
```env
VITE_API_URL=https://your-backend-url.railway.app
```

**Backend (в Railway/Render):**
```env
DATABASE_URL=postgresql://...
REDIS_URL=redis://...
TELEGRAM_API_ID=your_id
TELEGRAM_API_HASH=your_hash
SECRET_KEY=generate-strong-random-key-here
ENVIRONMENT=production
ALLOWED_ORIGINS=https://your-frontend-url.vercel.app
```

### 2. Обновите CORS настройки

В `backend/app/core/config.py` убедитесь что:
```python
ALLOWED_ORIGINS: List[str] = [
    "https://your-frontend-url.vercel.app",
    "https://your-frontend-url.onrender.com",
]
```

Или используйте переменную окружения:
```python
ALLOWED_ORIGINS: List[str] = settings.ALLOWED_ORIGINS.split(",") if settings.ALLOWED_ORIGINS else []
```

### 3. Database Migration

На продакшн сервере выполните:
```bash
# Railway
railway run alembic upgrade head

# Render (через SSH)
alembic upgrade head
```

---

## 🔐 Безопасность

1. **Никогда не коммитьте** `.env` файлы
2. Используйте **секреты** в GitHub Actions/Vercel/Railway
3. Генерируйте **сильные SECRET_KEY**:
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```
4. Настройте **rate limiting** на продакшн
5. Используйте **HTTPS** везде

---

## 📝 GitHub Actions CI/CD (Опционально)

Создайте `.github/workflows/deploy.yml` (уже создан)

---

## 🚀 Быстрый старт (TL;DR)

1. **GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/tgcursor2.git
   git push -u origin main
   ```

2. **Frontend на Vercel:**
   - Зайдите на vercel.com
   - Import → выберите репозиторий
   - Root: `frontend`
   - Framework: Vite
   - Deploy

3. **Backend на Railway:**
   - Зайдите на railway.app
   - New Project → GitHub repo
   - Root: `backend`
   - Добавьте PostgreSQL и Redis плагины
   - Добавьте переменные окружения
   - Deploy
   - Выполните миграции: `railway run alembic upgrade head`

4. **Обновите VITE_API_URL** в Vercel с Railway URL

5. **Готово!** 🎉

---

## 📚 Полезные ссылки

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [Render Documentation](https://render.com/docs)
- [GitHub Actions](https://docs.github.com/en/actions)


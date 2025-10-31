# 🚀 Быстрый старт: GitHub + Публичный деплой

## 📝 Инструкция по загрузке на GitHub и деплою

## 🌐 Варианты деплоя:

### Вариант 1: GitHub Pages (Frontend) + Railway/Render (Backend) ⭐ Бесплатно полностью

**Плюсы:** Полностью бесплатно, фронтенд на GitHub Pages, автоматический деплой из GitHub

#### Frontend на GitHub Pages:

1. **Включите GitHub Pages в репозитории:**
   - Перейдите в Settings → Pages
   - Source: **GitHub Actions**

2. **Настройте переменную окружения:**
   - Settings → Secrets and variables → Actions → New repository secret
   - Name: `VITE_API_URL`
   - Value: `https://your-backend-url.railway.app` (добавите после деплоя backend)

3. **GitHub Actions автоматически задеплоит:**
   - При каждом push в `main` ветку
   - Frontend будет доступен по адресу: `https://YOUR_USERNAME.github.io/tgcursor2/`

#### Backend на Railway/Render:

См. инструкцию ниже в разделе "Деплой Backend"

---

### Вариант 2: Vercel (Frontend) + Railway (Backend)

См. инструкцию ниже

---

## ✅ Что уже готово:

1. ✅ Обновлен `.gitignore` (исключает node_modules, .env, и т.д.)
2. ✅ Создан `vercel.json` для деплоя backend
3. ✅ Создан `Procfile` для Railway/Render
4. ✅ Создан CI/CD workflow (`.github/workflows/ci.yml`)
5. ✅ Создан GitHub Pages workflow (`.github/workflows/deploy-pages.yml`)
6. ✅ Добавлен `"type": "module"` в `package.json`
7. ✅ Настроен `base` в `vite.config.ts` для GitHub Pages
8. ✅ Создана документация по деплою (`DEPLOY_TO_PRODUCTION.md`, `GITHUB_DEPLOY.md`)

---

## 🚀 Пошаговая инструкция (GitHub Pages):

### Шаг 1: Загрузить на GitHub

```bash
# В директории проекта выполните:
cd C:\Users\Vasiliev\tgcursor2

# Инициализировать git (если еще не сделано)
git init

# Добавить все файлы
git add .

# Создать коммит
git commit -m "feat: готов к деплою с shadcn/ui дизайном и GitHub Pages"

# Создайте репозиторий на GitHub:
# 1. Перейдите на https://github.com/new
# 2. Название: tgcursor2
# 3. НЕ добавляйте README, .gitignore или лицензию
# 4. Скопируйте URL репозитория

# Привязать к удаленному репозиторию (замените YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/tgcursor2.git

# Переименовать ветку в main (если нужно)
git branch -M main

# Отправить код
git push -u origin main
```

---

### Шаг 2: Настроить GitHub Pages

1. **Перейдите в Settings репозитория**
2. **В левом меню выберите "Pages"**
3. **Source:** выберите **"GitHub Actions"**
4. **Сохраните**

---

### Шаг 3: Настроить Secrets для GitHub Actions

1. **Settings → Secrets and variables → Actions**
2. **New repository secret:**
   - Name: `VITE_API_URL`
   - Value: `https://your-backend-url.railway.app` 
   - *(Пока оставьте пустым или укажите позже после деплоя backend)*

---

### Шаг 4: Деплой Backend на Railway (10 минут)

1. **Перейдите на https://railway.app**
2. **Войдите через GitHub**
3. **Нажмите "New Project"**
4. **Выберите "Deploy from GitHub repo"**
5. **Выберите репозиторий** `tgcursor2`
6. **Настройки проекта:**
   - Нажмите на проект → Settings
   - Root Directory: **`backend`**
7. **Добавьте PostgreSQL:**
   - В проекте → New → Database → Add PostgreSQL
   - Railway автоматически создаст переменную `DATABASE_URL`
8. **Добавьте Redis:**
   - В проекте → New → Database → Add Redis
   - Railway автоматически создаст переменную `REDIS_URL`
9. **Настройте переменные окружения:**
   - Settings → Variables → New Variable:
     ```
     TELEGRAM_API_ID=your_api_id_here
     TELEGRAM_API_HASH=your_api_hash_here
     SECRET_KEY=сгенерируйте_случайный_ключ
     ENVIRONMENT=production
     ALLOWED_ORIGINS=https://YOUR_USERNAME.github.io,https://YOUR_USERNAME.github.io/tgcursor2
     ```
   - Для генерации SECRET_KEY:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     ```
10. **Настройте Start Command:**
    - Settings → Deploy → Start Command:
      ```
      uvicorn app.main:app --host 0.0.0.0 --port $PORT
      ```
11. **Выполните миграции:**
    - Railway → ваш проект → View Logs
    - Или используйте Railway CLI:
      ```bash
      railway login
      railway link
      railway run alembic upgrade head
      ```
12. **Deploy!**

**Результат:** Backend будет доступен по адресу типа `https://tgcursor2-production.up.railway.app`

---

### Шаг 5: Обновить Secrets и связать Frontend и Backend

1. **Скопируйте URL backend** из Railway (например: `https://tgcursor2-production.up.railway.app`)
2. **Обновите Secrets в GitHub:**
   - Settings → Secrets and variables → Actions
   - Обновите `VITE_API_URL` = `https://your-backend-url.railway.app`
3. **Обновите CORS в Railway:**
   - Settings → Variables
   - Обновите `ALLOWED_ORIGINS` = `https://YOUR_USERNAME.github.io,https://YOUR_USERNAME.github.io/tgcursor2`
4. **Запустите деплой вручную:**
   - Actions → Deploy Frontend to GitHub Pages → Run workflow

---

### Шаг 6: Готово! 🎉

Ваше приложение доступно по адресу:
- **Frontend:** https://YOUR_USERNAME.github.io/tgcursor2/
- **Backend API:** https://your-project.railway.app
- **API Docs:** https://your-project.railway.app/docs

---

## 🔄 Альтернатива: Vercel (Frontend) + Railway (Backend)

Если хотите использовать Vercel вместо GitHub Pages:

### Деплой Frontend на Vercel (5 минут)

1. **Перейдите на https://vercel.com**
2. **Войдите через GitHub**
3. **Нажмите "New Project"**
4. **Выберите репозиторий** `tgcursor2`
5. **Настройки:**
   - Framework Preset: **Vite**
   - Root Directory: **`frontend`**
   - Build Command: `npm run build` (уже по умолчанию)
   - Output Directory: `dist` (уже по умолчанию)
   - Install Command: `npm install` (уже по умолчанию)
6. **Environment Variables:**
   - `VITE_API_URL` = `https://your-backend-url.railway.app` 
   - *(Пока оставьте пустым, добавите после деплоя backend)*
7. **Нажмите "Deploy"**

**Результат:** Frontend будет доступен по адресу типа `https://tgcursor2.vercel.app`

---

### Шаг 3: Деплой Backend на Railway (10 минут)

1. **Перейдите на https://railway.app**
2. **Войдите через GitHub**
3. **Нажмите "New Project"**
4. **Выберите "Deploy from GitHub repo"**
5. **Выберите репозиторий** `tgcursor2`
6. **Настройки проекта:**
   - Нажмите на проект → Settings
   - Root Directory: **`backend`**
7. **Добавьте PostgreSQL:**
   - В проекте → New → Database → Add PostgreSQL
   - Railway автоматически создаст переменную `DATABASE_URL`
8. **Добавьте Redis:**
   - В проекте → New → Database → Add Redis
   - Railway автоматически создаст переменную `REDIS_URL`
9. **Настройте переменные окружения:**
   - Settings → Variables → New Variable:
     ```
     TELEGRAM_API_ID=your_api_id_here
     TELEGRAM_API_HASH=your_api_hash_here
     SECRET_KEY=сгенерируйте_случайный_ключ
     ENVIRONMENT=production
     ALLOWED_ORIGINS=https://your-frontend.vercel.app
     ```
   - Для генерации SECRET_KEY:
     ```bash
     python -c "import secrets; print(secrets.token_urlsafe(32))"
     ```
10. **Настройте Start Command:**
    - Settings → Deploy → Start Command:
      ```
      uvicorn app.main:app --host 0.0.0.0 --port $PORT
      ```
11. **Выполните миграции:**
    - Railway → ваш проект → View Logs
    - Или используйте Railway CLI:
      ```bash
      railway login
      railway link
      railway run alembic upgrade head
      ```
12. **Deploy!**

**Результат:** Backend будет доступен по адресу типа `https://tgcursor2-production.up.railway.app`

---

### Шаг 4: Связать Frontend и Backend

1. **Скопируйте URL backend** из Railway (например: `https://tgcursor2-production.up.railway.app`)
2. **Вернитесь в Vercel:**
   - Settings → Environment Variables
   - Обновите `VITE_API_URL` = `https://your-backend-url.railway.app`
   - Сохраните и нажмите "Redeploy"
3. **Обновите CORS в Railway:**
   - Settings → Variables
   - Обновите `ALLOWED_ORIGINS` = `https://your-frontend.vercel.app`

---

### Шаг 5: Готово! 🎉

Ваше приложение доступно по адресу:
- **Frontend:** https://your-project.vercel.app
- **Backend API:** https://your-project.railway.app
- **API Docs:** https://your-project.railway.app/docs

---

## 📋 Чеклист перед деплоем:

- [ ] Все файлы закоммичены в git
- [ ] Репозиторий создан на GitHub
- [ ] Код отправлен на GitHub (`git push`)
- [ ] Telegram API credentials получены (https://my.telegram.org/apps)
- [ ] SECRET_KEY сгенерирован
- [ ] Frontend задеплоен на Vercel
- [ ] Backend задеплоен на Railway
- [ ] PostgreSQL и Redis добавлены в Railway
- [ ] Миграции выполнены (`alembic upgrade head`)
- [ ] VITE_API_URL настроен в Vercel
- [ ] ALLOWED_ORIGINS настроен в Railway
- [ ] Приложение работает!

---

## 🆘 Решение проблем

### Frontend не подключается к Backend:
- Проверьте `VITE_API_URL` в Vercel (Settings → Environment Variables)
- Проверьте CORS настройки в backend (ALLOWED_ORIGINS)
- Убедитесь что backend доступен по HTTPS

### Backend выдает ошибки:
- Проверьте все переменные окружения в Railway
- Проверьте логи в Railway (View Logs)
- Убедитесь что миграции выполнены: `railway run alembic upgrade head`

### Database ошибки:
- Проверьте что PostgreSQL добавлен в Railway
- Проверьте `DATABASE_URL` в переменных окружения
- Выполните миграции: `railway run alembic upgrade head`

### CORS ошибки:
- Проверьте `ALLOWED_ORIGINS` в Railway
- Убедитесь что URL frontend точно совпадает (включая https://)
- Проверьте что backend настроен на правильный порт ($PORT)

---

## 💰 Стоимость:

- **Vercel:** Бесплатно (до 100GB bandwidth)
- **Railway:** Бесплатно $5 кредитов в месяц (достаточно для MVP)
- **Telegram API:** Бесплатно
- **Итого:** **$0** для старта! 🎉

---

## 📚 Дополнительные ресурсы:

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [GitHub Actions](https://docs.github.com/en/actions)

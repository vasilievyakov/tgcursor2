# 🚀 Варианты деплоя Backend

## 📊 Сравнение платформ

| Платформа | Цена | Сложность | Автодеплой | БД | Производительность | Рекомендация |
|-----------|------|-----------|------------|-----|-------------------|--------------|
| **Railway** | Бесплатно ($5/мес) | ⭐ Легко | ✅ GitHub | ✅ PostgreSQL, Redis | ⭐⭐⭐⭐ | 🥇 **Лучший выбор** |
| **Render** | Бесплатно (750ч/мес) | ⭐ Легко | ✅ GitHub | ✅ PostgreSQL, Redis | ⭐⭐⭐ | 🥈 Хорошо |
| **Fly.io** | Бесплатно (3 VMs) | ⭐⭐ Средне | ✅ GitHub | ⚠️ Нужна настройка | ⭐⭐⭐⭐⭐ | 🥉 Продвинутый |
| **DigitalOcean** | $5/мес | ⭐ Легко | ✅ GitHub | ✅ PostgreSQL, Redis | ⭐⭐⭐⭐ | 💰 Платный |
| **PythonAnywhere** | Бесплатно/платно | ⭐⭐⭐ Сложно | ❌ Ручной | ⚠️ Ограничено | ⭐⭐ | ⚠️ Не рекомендуется |

---

## 🥇 1. Railway (РЕКОМЕНДУЕТСЯ)

### Плюсы:
- ✅ **Бесплатно**: $5 кредитов в месяц (хватает для MVP)
- ✅ **Автоматический деплой** из GitHub
- ✅ **Встроенные PostgreSQL и Redis** (1 клик)
- ✅ **Очень простая настройка** (5 минут)
- ✅ **Отличная документация**
- ✅ **HTTPS автоматически**
- ✅ **Мониторинг и логи**

### Минусы:
- ⚠️ Платный тариф после $5 кредитов

### Быстрый старт:
1. Зайдите на https://railway.app
2. Войдите через GitHub
3. New Project → Deploy from GitHub repo
4. Выберите `vasilievyakov/tgcursor2`
5. Settings → Root Directory: `backend`
6. Добавьте PostgreSQL и Redis
7. Настройте переменные окружения
8. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

**Время настройки:** 5-10 минут  
**Стоимость:** $0 для старта

---

## 🥈 2. Render

### Плюсы:
- ✅ **Бесплатно**: 750 часов/месяц
- ✅ **Автоматический деплой** из GitHub
- ✅ **Встроенные PostgreSQL и Redis**
- ✅ **HTTPS автоматически**
- ✅ **Простая настройка**

### Минусы:
- ⚠️ **Сервис засыпает** после 15 минут бездействия (первый запрос долгий)
- ⚠️ Медленнее Railway

### Быстрый старт:
1. Зайдите на https://render.com
2. Войдите через GitHub
3. New → Web Service
4. Подключите репозиторий `vasilievyakov/tgcursor2`
5. Настройки:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Добавьте PostgreSQL и Redis
7. Настройте переменные окружения

**Время настройки:** 10-15 минут  
**Стоимость:** $0

---

## 🥉 3. Fly.io

### Плюсы:
- ✅ **Бесплатно**: 3 shared-cpu VMs
- ✅ **Отличная производительность**
- ✅ **Глобальное распределение** (близко к пользователям)
- ✅ **Не засыпает** (всегда онлайн)
- ✅ **Автоматический деплой** из GitHub
- ✅ **Dockerfile уже есть** ✅

### Минусы:
- ⚠️ Требует больше настройки
- ⚠️ PostgreSQL и Redis нужно настраивать отдельно

### Быстрый старт:
1. Установите Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Зайдите на https://fly.io и войдите
3. `fly launch` в директории `backend`
4. Настройте `fly.toml`
5. Добавьте PostgreSQL: `fly postgres create`
6. Добавьте Redis: `fly redis create`
7. `fly deploy`

**Время настройки:** 15-20 минут  
**Стоимость:** $0

---

## 💰 4. DigitalOcean App Platform

### Плюсы:
- ✅ **Профессиональный сервис**
- ✅ **Автоматический деплой** из GitHub
- ✅ **Встроенные PostgreSQL и Redis**
- ✅ **Отличная производительность**
- ✅ **Не засыпает**

### Минусы:
- ⚠️ **Платный**: минимум $5/месяц
- ⚠️ Нет бесплатного тарифа

### Быстрый старт:
1. Зайдите на https://cloud.digitalocean.com
2. App Platform → Create App
3. Подключите GitHub репозиторий
4. Настройте:
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Добавьте PostgreSQL и Redis
6. Настройте переменные окружения

**Время настройки:** 10-15 минут  
**Стоимость:** $5/месяц

---

## ⚠️ 5. PythonAnywhere

### Плюсы:
- ✅ Бесплатный тариф для начинающих
- ✅ Специализирован для Python

### Минусы:
- ⚠️ Требует много ручной настройки
- ⚠️ Ограниченный бесплатный тариф
- ⚠️ Нет автоматического деплоя из GitHub
- ⚠️ Нет встроенных PostgreSQL/Redis

**Не рекомендуется для этого проекта**

---

## 🎯 Рекомендация

### Для MVP / Демо:
**Railway** — лучший выбор:
- Быстрая настройка (5 минут)
- Бесплатно для старта
- Всё работает из коробки

### Для продакшн с бюджетом:
**Fly.io** или **DigitalOcean**:
- Лучшая производительность
- Не засыпает
- Профессиональный сервис

### Для тестирования:
**Render**:
- Бесплатно
- Простая настройка
- Подходит для тестов

---

## 📋 Что нужно для любого варианта:

1. **Telegram API credentials:**
   - Получите на https://my.telegram.org/apps
   - `TELEGRAM_API_ID`
   - `TELEGRAM_API_HASH`

2. **SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

3. **ALLOWED_ORIGINS:**
   ```
   https://vasilievyakov.github.io,https://vasilievyakov.github.io/tgcursor2
   ```

4. **Миграции БД:**
   ```bash
   alembic upgrade head
   ```

---

## 🔄 После деплоя:

1. Получите URL backend (например: `https://your-app.railway.app`)
2. Обновите `VITE_API_URL` secret в GitHub:
   ```bash
   gh secret set VITE_API_URL --body "https://your-backend-url.railway.app" --repo vasilievyakov/tgcursor2
   ```
3. Перезапустите frontend workflow:
   ```bash
   gh workflow run deploy-pages.yml --repo vasilievyakov/tgcursor2
   ```

---

## ❓ Какой выбрать?

**Если нужно быстро и бесплатно:** Railway  
**Если нужна производительность:** Fly.io  
**Если есть бюджет:** DigitalOcean  
**Если Railway не подходит:** Render


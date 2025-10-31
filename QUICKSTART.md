# Инструкция по запуску проекта

## Предварительные требования

### 1. Установка Docker

**Windows:**
1. Скачайте и установите [Docker Desktop для Windows](https://www.docker.com/products/docker-desktop/)
2. После установки перезапустите компьютер
3. Запустите Docker Desktop

**Проверка установки:**
```powershell
docker --version
docker compose version
```

### 2. Настройка переменных окружения

Файл `.env` уже создан из `env.example`. Вам нужно заполнить:

**Обязательные переменные:**
- `TELEGRAM_API_ID` - получите на https://my.telegram.org/apps
- `TELEGRAM_API_HASH` - получите на https://my.telegram.org/apps

**Для тестирования можно использовать временные значения:**
```env
TELEGRAM_API_ID=12345678
TELEGRAM_API_HASH=your_api_hash_here
```

### 3. Запуск проекта

После установки Docker:

```powershell
# Проверка Docker
docker --version
docker compose version

# Запуск всех сервисов
docker compose up -d --build

# Выполнение миграций базы данных
docker compose exec backend alembic upgrade head

# Проверка статуса
docker compose ps

# Просмотр логов
docker compose logs -f
```

### 4. Доступ к сервисам

После успешного запуска:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Документация**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 5. Остановка проекта

```powershell
# Остановка всех сервисов
docker compose down

# Остановка с удалением volumes (удалит данные БД)
docker compose down -v
```

## Troubleshooting

### Docker не найден

Если команда `docker` не найдена:
1. Убедитесь, что Docker Desktop установлен и запущен
2. Перезапустите PowerShell/терминал
3. Проверьте, что Docker Desktop работает: иконка в трее должна быть зеленая

### Порты заняты

Если порты 3000, 8000, 5432 или 6379 заняты:
1. Измените порты в `docker-compose.yml`
2. Или остановите сервисы, использующие эти порты

### Ошибки при сборке

```powershell
# Очистка и пересборка
docker compose down
docker compose build --no-cache
docker compose up -d
```

### Проблемы с базой данных

```powershell
# Пересоздание базы данных
docker compose down -v
docker compose up -d
docker compose exec backend alembic upgrade head
```

## Быстрый старт (после установки Docker)

```powershell
# 1. Заполните TELEGRAM_API_ID и TELEGRAM_API_HASH в .env файле

# 2. Запустите проект
docker compose up -d --build

# 3. Дождитесь запуска (30-60 секунд)

# 4. Выполните миграции
docker compose exec backend alembic upgrade head

# 5. Откройте в браузере
# Frontend: http://localhost:3000
# API Docs: http://localhost:8000/docs
```

## Что дальше?

1. Откройте http://localhost:3000 в браузере
2. Добавьте первый Telegram канал
3. Дождитесь парсинга данных
4. Просмотрите посты в таблице
5. Попробуйте фильтры и экспорт

Удачи! 🚀




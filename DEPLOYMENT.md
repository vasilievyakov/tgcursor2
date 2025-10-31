# Deployment Guide

## Подготовка к деплою

### 1. Настройка переменных окружения

Создайте файл `.env.prod` на основе `env.prod.example`:

```bash
cp env.prod.example .env.prod
# Отредактируйте .env.prod и заполните все значения
```

**Важно**: 
- Используйте сильные пароли для базы данных
- Сгенерируйте случайный SECRET_KEY (можно использовать `openssl rand -hex 32`)
- Получите Telegram API credentials на https://my.telegram.org/apps

### 2. Настройка SSL сертификата

#### Вариант 1: Let's Encrypt (рекомендуется)

```bash
# Установите certbot
sudo apt-get update
sudo apt-get install certbot

# Получите сертификат
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# Скопируйте сертификаты в nginx/ssl
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/
sudo chmod 644 nginx/ssl/fullchain.pem
sudo chmod 600 nginx/ssl/privkey.pem

# Настройте автообновление (cron)
sudo certbot renew --dry-run
```

#### Вариант 2: Self-signed (для тестирования)

```bash
mkdir -p nginx/ssl
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout nginx/ssl/privkey.pem \
  -out nginx/ssl/fullchain.pem
```

### 3. Настройка домена

Обновите DNS записи для вашего домена:
- A запись: `yourdomain.com` -> ваш IP сервера
- A запись: `www.yourdomain.com` -> ваш IP сервера

### 4. Дескриптор деплоя

```bash
# Сделайте скрипт исполняемым
chmod +x scripts/deploy.sh
chmod +x scripts/backup.sh

# Запустите деплой
./scripts/deploy.sh
```

## Проверка работоспособности

После деплоя проверьте:

1. **Frontend**: https://yourdomain.com
2. **API Health**: https://yourdomain.com/health
3. **API Docs**: https://yourdomain.com/docs
4. **Логи**: 
   ```bash
   docker-compose -f docker-compose.prod.yml logs -f
   ```

## Мониторинг

### Просмотр логов

```bash
# Все сервисы
docker-compose -f docker-compose.prod.yml logs -f

# Конкретный сервис
docker-compose -f docker-compose.prod.yml logs -f backend
docker-compose -f docker-compose.prod.yml logs -f celery
```

### Мониторинг ресурсов

```bash
# Статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# Использование ресурсов
docker stats
```

## Backup

### Автоматический backup

Настройте cron для автоматического backup:

```bash
# Добавьте в crontab
crontab -e

# Запуск backup каждый день в 2:00
0 2 * * * /path/to/project/scripts/backup.sh
```

### Ручной backup

```bash
./scripts/backup.sh
```

### Восстановление из backup

```bash
# Распакуйте backup
gunzip backups/backup_YYYYMMDD_HHMMSS.sql.gz

# Восстановите
docker-compose exec -T postgres psql -U postgres tgcursor2 < backups/backup_YYYYMMDD_HHMMSS.sql
```

## Обновление

Для обновления приложения:

```bash
# Остановите сервисы
docker-compose -f docker-compose.prod.yml down

# Обновите код
git pull

# Пересоберите и запустите
./scripts/deploy.sh
```

## Troubleshooting

### Проблемы с SSL

Если SSL не работает, проверьте:
1. Сертификаты в `nginx/ssl/`
2. Права доступа к файлам
3. Конфигурацию nginx

### Проблемы с подключением к БД

Проверьте:
1. Переменные окружения DATABASE_URL
2. Состояние контейнера postgres
3. Логи: `docker-compose logs postgres`

### Высокое использование памяти

Уменьшите количество workers:
```yaml
# В docker-compose.prod.yml
command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2
```

## Безопасность

1. ✅ Используйте сильные пароли
2. ✅ Регулярно обновляйте зависимости
3. ✅ Настройте firewall (UFW)
4. ✅ Регулярно делайте backup
5. ✅ Мониторьте логи на подозрительную активность
6. ✅ Настройте rate limiting в nginx
7. ✅ Используйте HTTPS только
8. ✅ Регулярно обновляйте SSL сертификаты

## Масштабирование

Для масштабирования можно:
1. Увеличить количество workers в backend
2. Добавить еще Celery workers
3. Использовать load balancer перед несколькими инстансами
4. Настроить Redis для кэширования
5. Использовать CDN для статических файлов


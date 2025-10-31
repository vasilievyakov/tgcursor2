## ⚠️ Docker не установлен

Для запуска проекта необходимо установить Docker Desktop.

### Шаги для запуска:

1. **Установите Docker Desktop:**
   - Windows: https://www.docker.com/products/docker-desktop/
   - После установки перезапустите компьютер
   - Запустите Docker Desktop (иконка в трее должна быть зеленая)

2. **Заполните переменные окружения:**
   - Откройте файл `.env`
   - Заполните `TELEGRAM_API_ID` и `TELEGRAM_API_HASH`
   - Получите их на https://my.telegram.org/apps

3. **Запустите проект:**
   ```powershell
   docker compose up -d --build
   ```

4. **Выполните миграции:**
   ```powershell
   docker compose exec backend alembic upgrade head
   ```

5. **Откройте в браузере:**
   - Frontend: http://localhost:3000
   - API Docs: http://localhost:8000/docs

### Альтернативный запуск без Docker

Если Docker установить нельзя, можно запустить локально:

**Backend:**
```powershell
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

**Frontend:**
```powershell
cd frontend
npm install
npm run dev
```

Но потребуется настроить PostgreSQL и Redis отдельно.

Подробные инструкции в [QUICKSTART.md](./QUICKSTART.md)




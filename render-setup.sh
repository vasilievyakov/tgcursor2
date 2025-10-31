#!/bin/bash
# Render Auto-Setup Script Helper
# Этот скрипт поможет быстро настроить переменные окружения

echo "🎨 Render Auto-Setup Helper"
echo ""
echo "Скопируйте эти переменные в Render Web Service → Environment Variables:"
echo ""
echo "DATABASE_URL=<Internal Database URL из PostgreSQL>"
echo "REDIS_URL=<Internal Redis URL из Redis>"
echo "TELEGRAM_API_ID=your_api_id_here"
echo "TELEGRAM_API_HASH=your_api_hash_here"
echo "SECRET_KEY=EkwFPxdpx5UjpDQoLOWapV6s9S2JIgymY_Ev-6wdoAw"
echo "ENVIRONMENT=production"
echo "ALLOWED_ORIGINS=https://vasilievyakov.github.io,https://vasilievyakov.github.io/tgcursor2"
echo ""
echo "После настройки всех переменных, Render автоматически задеплоит приложение!"


# Максимально автоматизированная настройка Render
# Этот скрипт делает все что возможно автоматически

param(
    [string]$PostgresUrl = "",
    [string]$RedisUrl = "",
    [string]$TelegramApiId = "",
    [string]$TelegramApiHash = ""
)

Write-Host "🚀 Render Auto-Complete Setup" -ForegroundColor Cyan
Write-Host ""

# Генерируем SECRET_KEY если нужно
$secretKey = "EkwFPxdpx5UjpDQoLOWapV6s9S2JIgymY_Ev-6wdoAw"

# Открываем все страницы
Write-Host "📋 Открываю страницы Render..." -ForegroundColor Yellow
Start-Process "https://dashboard.render.com/new/postgres"
Start-Sleep -Seconds 2
Start-Process "https://dashboard.render.com/new/redis"
Start-Sleep -Seconds 2
Start-Process "https://dashboard.render.com/web/new"
Start-Sleep -Seconds 2

Write-Host "✅ Страницы открыты!" -ForegroundColor Green

# Создаем файл с готовыми переменными
$envContent = @"
# Render Environment Variables
# Скопируйте эти переменные в Render Web Service → Environment Variables

DATABASE_URL=$PostgresUrl
REDIS_URL=$RedisUrl
TELEGRAM_API_ID=$TelegramApiId
TELEGRAM_API_HASH=$TelegramApiHash
SECRET_KEY=$secretKey
ENVIRONMENT=production
ALLOWED_ORIGINS=https://vasilievyakov.github.io,https://vasilievyakov.github.io/tgcursor2
"@

$envContent | Out-File -FilePath "RENDER_FINAL_ENV.txt" -Encoding UTF8

Write-Host ""
Write-Host "✅ Создан файл RENDER_FINAL_ENV.txt с переменными!" -ForegroundColor Green
Write-Host ""

# Показываем инструкции
Write-Host "📋 АВТОМАТИЧЕСКАЯ НАСТРОЙКА:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣ PostgreSQL (открыта в браузере):" -ForegroundColor Yellow
Write-Host "   • Заполните форму и нажмите 'Create Database'" -ForegroundColor White
Write-Host "   • Скопируйте Internal Database URL" -ForegroundColor White
Write-Host ""
Write-Host "2️⃣ Redis (открыта в браузере):" -ForegroundColor Yellow
Write-Host "   • Заполните форму и нажмите 'Create Redis'" -ForegroundColor White
Write-Host "   • Скопируйте Internal Redis URL" -ForegroundColor White
Write-Host ""
Write-Host "3️⃣ Web Service (открыта в браузере):" -ForegroundColor Yellow
Write-Host "   • Подключите GitHub repo: vasilievyakov/tgcursor2" -ForegroundColor White
Write-Host "   • Заполните форму и нажмите 'Create Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "4️⃣ Добавьте переменные:" -ForegroundColor Yellow
Write-Host "   • Откройте RENDER_FINAL_ENV.txt" -ForegroundColor White
Write-Host "   • Скопируйте переменные в Render" -ForegroundColor White
Write-Host ""

Write-Host "💡 После создания сервисов Render автоматически начнет деплой!" -ForegroundColor Green
Write-Host ""

# Показываем готовые переменные
Write-Host "📄 Переменные окружения:" -ForegroundColor Cyan
Write-Host $envContent -ForegroundColor White


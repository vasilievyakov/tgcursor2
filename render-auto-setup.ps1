# Render Auto-Setup PowerShell Script
# Этот скрипт поможет автоматизировать настройку Render

Write-Host "🎨 Render Auto-Setup" -ForegroundColor Cyan
Write-Host ""

# Переменные окружения
$envVars = @{
    "TELEGRAM_API_ID" = "your_api_id_here"
    "TELEGRAM_API_HASH" = "your_api_hash_here"
    "SECRET_KEY" = "EkwFPxdpx5UjpDQoLOWapV6s9S2JIgymY_Ev-6wdoAw"
    "ENVIRONMENT" = "production"
    "ALLOWED_ORIGINS" = "https://vasilievyakov.github.io,https://vasilievyakov.github.io/tgcursor2"
}

Write-Host "📋 Переменные окружения для Render:" -ForegroundColor Yellow
Write-Host ""
foreach ($key in $envVars.Keys) {
    Write-Host "$key=$($envVars[$key])" -ForegroundColor White
}

Write-Host ""
Write-Host "🔗 Открываю страницы Render..." -ForegroundColor Cyan

# Открываем страницы
Start-Process "https://dashboard.render.com/new/postgres"
Start-Sleep -Seconds 2
Start-Process "https://dashboard.render.com/new/redis"
Start-Sleep -Seconds 2
Start-Process "https://dashboard.render.com/web/new"
Start-Sleep -Seconds 2

Write-Host ""
Write-Host "✅ Открыты страницы для создания:" -ForegroundColor Green
Write-Host "   • PostgreSQL" -ForegroundColor White
Write-Host "   • Redis" -ForegroundColor White
Write-Host "   • Web Service" -ForegroundColor White

Write-Host ""
Write-Host "📝 Инструкции:" -ForegroundColor Yellow
Write-Host "1. Создайте PostgreSQL (уже открыта в браузере)" -ForegroundColor White
Write-Host "2. Создайте Redis (уже открыта в браузере)" -ForegroundColor White
Write-Host "3. Создайте Web Service (уже открыта в браузере)" -ForegroundColor White
Write-Host "4. Добавьте переменные окружения (скопируйте выше)" -ForegroundColor White

Write-Host ""
Write-Host "💡 После создания всех сервисов, переменные будут готовы к копированию!" -ForegroundColor Cyan


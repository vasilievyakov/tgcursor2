# GitHub Pages: Полная инструкция

## ✅ Что настроено:

1. ✅ GitHub Actions workflow (`.github/workflows/deploy-pages.yml`)
2. ✅ Vite base path (`/tgcursor2/` в `vite.config.ts`)
3. ✅ React Router basename (автоматически определяется в `App.tsx`)
4. ✅ GitHub Actions секреты для `VITE_API_URL`

---

## 🚀 Быстрый старт с GitHub Pages:

### Шаг 1: Загрузить код на GitHub

```bash
git add .
git commit -m "feat: добавлена поддержка GitHub Pages"
git push origin main
```

### Шаг 2: Настроить GitHub Pages

1. Перейдите в **Settings** вашего репозитория
2. В левом меню выберите **Pages**
3. В разделе **Source** выберите **"GitHub Actions"**
4. Сохраните

### Шаг 3: Настроить Secrets

1. **Settings → Secrets and variables → Actions**
2. **New repository secret:**
   - Name: `VITE_API_URL`
   - Value: `https://your-backend-url.railway.app`
   - *(Добавите после деплоя backend)*

### Шаг 4: Запустить деплой

1. Перейдите в **Actions** в репозитории
2. Выберите workflow **"Deploy Frontend to GitHub Pages"**
3. Нажмите **"Run workflow"** → **"Run workflow"**

Или просто сделайте push в `main` ветку - деплой запустится автоматически!

---

## 📝 Изменение base path

Если имя репозитория НЕ `tgcursor2`, нужно изменить:

1. **В `vite.config.ts`:**
   ```ts
   base: process.env.NODE_ENV === 'production' ? '/ВАШЕ_ИМЯ_РЕПОЗИТОРИЯ/' : '/',
   ```

2. **В `App.tsx` функция `getBasePath()`:**
   ```ts
   if (pathname.includes('/ВАШЕ_ИМЯ_РЕПОЗИТОРИЯ/')) {
     return '/ВАШЕ_ИМЯ_РЕПОЗИТОРИЯ';
   }
   ```

3. **В Railway ALLOWED_ORIGINS:**
   ```
   ALLOWED_ORIGINS=https://YOUR_USERNAME.github.io,https://YOUR_USERNAME.github.io/ВАШЕ_ИМЯ_РЕПОЗИТОРИЯ
   ```

---

## 🔍 Как это работает:

1. **GitHub Actions** автоматически собирает frontend при каждом push
2. **Vite** собирает проект с base path `/tgcursor2/`
3. **React Router** использует basename для правильной маршрутизации
4. **GitHub Pages** раздает статические файлы из `dist/`

---

## 🌐 URL структура:

- Главная: `https://YOUR_USERNAME.github.io/tgcursor2/`
- Посты: `https://YOUR_USERNAME.github.io/tgcursor2/posts`
- Каналы: `https://YOUR_USERNAME.github.io/tgcursor2/`

---

## ⚠️ Важно:

1. **Имя репозитория:** Убедитесь что имя репозитория совпадает с base path (`tgcursor2`)
2. **CORS:** Обновите `ALLOWED_ORIGINS` в backend с GitHub Pages URL
3. **Secrets:** Всегда используйте Secrets для чувствительных данных
4. **HTTPS:** GitHub Pages автоматически предоставляет HTTPS

---

## 🆘 Решение проблем:

### Ссылки не работают:
- Проверьте что `base` в `vite.config.ts` правильный
- Проверьте что `basename` в Router правильный
- Убедитесь что используете `<Link>` из react-router-dom

### Стили не загружаются:
- Проверьте что `base` path правильный
- Проверьте пути к CSS файлам в `index.html`

### API не работает:
- Проверьте `VITE_API_URL` в Secrets
- Проверьте CORS настройки в backend
- Проверьте что backend доступен по HTTPS


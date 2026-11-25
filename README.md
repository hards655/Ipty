# Ipty — ReDroid Android 15

Android 15 (API 35), официальный образ ReDroid, x86_64 на GitHub Actions. Это контейнер Android, не Samsung One UI. ADB доступен только на loopback хоста; для работы нужен Linux с Binder и Docker.

## Запуск
GitHub Actions: ReDroid Android 15 запускается при push в main или вручную. После теста контейнер выключается. Артефакт redroid-android15-results содержит реальные скриншоты и логи, если загрузка успешна.

Локально на совместимом Linux: установите Docker Compose и adb, загрузите модуль binder_linux, затем выполните docker compose up -d и bash scripts/test-android.sh. Для остановки: docker compose down.

## Приложение
Положите собственный тестовый APK в app/app.apk. При необходимости укажите имя пакета в app/package.txt. Скрипт устанавливает APK, запускает launcher activity и сохраняет results/app-launch.png. Если APK нет, сохраняется только results/android-home.png и сообщение app-status.txt. Не загружайте секретные APK в публичный репозиторий.

## Профиль
Разрешение 1080×2340, DPI 420 и отображаемое имя SM-S911B-LAB. profile.properties сохранён как справочный профиль; реальные свойства Android и состояние безопасности не подменяются. GitHub-hosted runner может не предоставлять Binder; тогда потребуется совместимый Linux runner.

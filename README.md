# Android 15 / dm1q reference lab

Официальный Android 15 (API 35) в Android Emulator x86_64. Профиль Galaxy S23 SM-S911B используется только для сравнения свойств.

## GitHub Actions
Workflow Android 15 boot test запускается при push в main или вручную через Actions. Он устанавливает официальный образ Google APIs, загружает Android без окна, проверяет API 35, сравнивает свойства и сохраняет скриншот и логи в артефакт. После завершения задания виртуальная машина выключается: это не постоянный облачный телефон.

## Локальный запуск
Требования: Python 3.9+, Android SDK Command-line Tools, JDK, аппаратная виртуализация и свободное место. Укажите ANDROID_HOME или ANDROID_SDK_ROOT.

```sh
python lab.py setup
python lab.py run
```

Во втором терминале после загрузки:
```sh
python lab.py compare
```

При нескольких эмуляторах укажите --serial emulator-5554 с фактическим serial.

## Ограничения
profile.properties — 61 эталонный параметр, не активная конфигурация. Это не One UI, не прошивка Samsung и не физическая платформа Snapdragon. Скрипт не подменяет системные свойства, состояние Verified Boot, Knox или аттестацию. Наличие ARM-трансляции зависит от официального образа.

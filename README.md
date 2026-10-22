# Учебное облачное хранилище данных

Небольшой учебный прототип для работы с записями через HTTP API. Сейчас хранилище локальное; подключение настоящего облачного объектного хранилища можно добавить отдельно.

## Архитектура

| Компонент | Назначение | Взаимодействие |
| --- | --- | --- |
| Клиент | Отправляет HTTP-запросы и получает JSON-ответы | Обращается к API приложения |
| API-приложение | Проверяет запросы и обрабатывает записи | Читает и обновляет JSON-файл |
| Хранилище данных | Сохраняет учебные записи в data/items.json | Доступно приложению через файловую систему |
| Конфигурация | Задаёт путь через CLOUD_STORAGE_PATH | Читается приложением при запуске |

Подробная схема приведена в [документе архитектуры](docs/architecture.md).

## Структура репозитория

~~~text
.
├── app/main.py              # HTTP API учебного прототипа
├── config/example.env       # Безопасный пример настройки
├── data/items.json          # Начальное пустое хранилище
├── docs/architecture.md     # Компоненты и взаимодействие
├── REPORT_LAB3.md           # Отчёт по командной работе
├── REPORT_LAB4.md           # Отчёт по Markdown-документации
└── README.md
~~~

## Технологии

- **Python 3.10+** — HTTP-сервер и JSON на стандартной библиотеке.
- **Git и GitHub** — история изменений и совместная разработка.
- **Markdown** — документация проекта.

Сторонние Python-пакеты не требуются. Внешний облачный сервис пока не подключён.

## Запуск

1. Установите Python 3.10 или новее.
2. Склонируйте репозиторий и перейдите в каталог проекта:

~~~bash
git clone https://github.com/ersss3530/cloud-storage-coursework-ersss3530.git
cd cloud-storage-coursework-ersss3530
~~~

3. При необходимости задайте путь к хранилищу. По умолчанию используется data/items.json.

PowerShell:

~~~powershell
$env:CLOUD_STORAGE_PATH = "./data/items.json"
~~~

Bash:

~~~bash
export CLOUD_STORAGE_PATH=./data/items.json
~~~

4. Запустите API:

~~~bash
python app/main.py
~~~

Сервер будет доступен по адресу http://127.0.0.1:8000. Для остановки нажмите Ctrl+C.

## Использование API

Проверка состояния:

~~~bash
curl http://127.0.0.1:8000/health
~~~

Получение записей:

~~~bash
curl http://127.0.0.1:8000/items
~~~

Добавление записи:

~~~bash
curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Лекция 1","description":"Материалы курса"}'
~~~

API принимает JSON-объект с обязательным непустым полем name и необязательным полем description. Файловое хранилище служит только учебной демонстрацией.

## Командная работа

Состав участников и их GitHub-логины указываются после согласования команды. Не публикуйте пароли, токены и ключи доступа. План Issues, ветвей и PR приведён в [отчёте лабораторной №3](REPORT_LAB3.md).

## Полезные ссылки

- [GitHub: документация о README](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- [GitHub: синтаксис Markdown](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)

# CastLoader

CastLoader - это инструмент командной строки для загрузки подкастов из RSS-фидов. Проект позволяет пользователям просматривать список подкастов, выбирать те, которые они хотят загрузить, и скачивать их в указанную директорию.

Проект был создан для загрузки подкастов на MP3 плееры, которые часто сортируют подкасты не по имени файла, а по дате создания файла. Поэтому выбранные файлы загружаются именно в однопоточном режиме и в порядке выхода. Т.е. сначала будет загружен самый старый подкаст из выбранных, затем новее и т.д. до самого нового.

## Особенности

- Просмотр списка подкастов из RSS-фида.
- Выбор подкастов для загрузки.
- Загрузка подкастов в указанную директорию.
- Интерактивный интерфейс с использованием библиотеки `curses`.

## Требования

- Python 3.6 или выше
- Библиотеки: `feedparser`, `requests`, `curses`

## Установка

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/yourusername/CastLoader.git
   cd CastLoader
   ```

2. Установите необходимые зависимости:
   ```bash
   pip3 install -r requirements.txt
   ```

## Использование

Запустите скрипт с указанием URL RSS-фида и, при необходимости, пути для сохранения подкастов:

```bash
python castloader.py <feed_url> [save_path]
```

Путь может быть как относительный, так и абсолютный.

### Примеры

1. Загрузка подкастов из фида и сохранение в текущую директорию:
   ```bash
   python castloader.py http://example.com/podcast/feed
   ```

2. Загрузка подкастов из фида и сохранение в указанную директорию:
   ```bash
   python castloader.py http://example.com/podcast/feed /path/to/save/podcasts
   ```

## Команды интерфейса

- `n` - Следующая страница
- `p` - Предыдущая страница
- `↑`/`↓` - Навигация вверх/вниз
- `s` - Выбрать/отменить выбор подкаста
- `a` - Выбрать все подкасты на текущей странице
- `d` - Начать загрузку выбранных подкастов
- `q` - Выйти из программы

## Лицензия

Этот проект лицензирован под [MIT License](LICENSE).

## Авторы

- Evgeniy Shumilov <evgeniy.shumilov@gmail.com>


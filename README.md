Что это за проект:
Yatube - это социальная сеть для блогеров.

Какие задачи решает:
- Помогает молодым писателям заявить о себе.
- Помогает молодым программерам заявить о себе.


Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

git clone https://github.com/yandex-praktikum/kittygram.git

cd kittygram

Cоздать и активировать виртуальное окружение:

python3 -m venv venv

source venv/bin/activate

Установить зависимости из файла requirements.txt:

python3 -m pip install --upgrade pip

pip install -r requirements.txt

Выполнить миграции:

python3 manage.py migrate

Запустить проект:

python3 manage.py runserver

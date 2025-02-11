# Используем официальный образ Python в качестве базового
FROM python:3.13.2-alpine3.21

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /code

# Копируем название зависимостей
COPY requirements.txt requirements.txt

# Устанавливаем зависимости
RUN pip install -r requirements.txt

# Копируем файлы проекта в контейнер
COPY . .

# Команда для запуска user-бота
CMD ["python", "-u", "run.py"]
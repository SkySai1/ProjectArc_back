# Используем базовый образ Python
FROM python:3.10-slim

COPY data/ data/

# Устанавливаем рабочую директорию
WORKDIR /data


# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Указываем команду запуска
CMD ["python", "run.py"]

# Используем базовый образ Python
FROM python:3.10-slim

# Устанавливаем gosu для переключения пользователя
RUN apt-get update && apt-get install -y gosu && rm -rf /var/lib/apt/lists/*

# Создаем директорию для приложения
WORKDIR /data

# Копируем файлы приложения
COPY data/ /data

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем и даем права на entrypoint.sh
COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Указываем точку входа
ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]

# Указываем команду запуска
CMD ["python", "run.py"]

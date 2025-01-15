#!/bin/bash
set -e

# Проверяем, заданы ли UID и GID
if [ -z "$HOST_UID" ] || [ -z "$HOST_GID" ]; then
  echo "Не заданы переменные HOST_UID и HOST_GID"
  exit 1
fi

# Проверяем, существует ли группа с GID, если нет - создаём
if ! getent group "$HOST_GID" > /dev/null; then
  groupadd -g "$HOST_GID" appgroup
else
  groupadd -g "$HOST_GID" appgroup || true
fi

# Проверяем, существует ли пользователь с UID, если нет - создаём
if ! id -u "appuser" &>/dev/null; then
  useradd -u "$HOST_UID" -g "$HOST_GID" -m appuser
fi

# Изменяем владельца директории /data
chown -R appuser:appgroup /data

# Проверяем права доступа
echo "Права на /data:"
ls -ld /data

# Переключаемся на нового пользователя и выполняем команду
exec gosu appuser "$@"

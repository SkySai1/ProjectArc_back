# Описание маршрутов "History"

Директория `app/routes/history` содержит маршруты для управления историей изменений в проекте. Все маршруты используют `Blueprint` для модульности и удобства масштабирования.

## Подключение
Для регистрации маршрутов в приложении используется файл `app/__init__.py`:
```python
from app.routes.history import history_bp
app.register_blueprint(history_bp, url_prefix='/history')
```

## Маршруты

### 1. **GET /history/**
**Описание:** Получение истории изменений.

- **Параметры:** отсутствуют.
- **Ответы:**
  - `200 OK` – Возвращает JSON с историей изменений.
  - `404 Not Found` – Лог-файл истории отсутствует.

Пример ответа:
```json
[
    {
        "timestamp": 1671234567,
        "description": "Создан новый файл.",
        "affected_files": ["file1.py", "file2.py"]
    }
]
```

---

### 2. **POST /history/**
**Описание:** Запись изменения в историю.

- **Параметры (JSON):**
  - `description` (string, обязательный) – Описание изменения.
  - `affected_files` (list, необязательный) – Список затронутых файлов.

- **Ответы:**
  - `201 Created` – Изменение успешно записано.
  - `400 Bad Request` – Отсутствует обязательный параметр `description`.

Пример запроса:
```json
{
    "description": "Обновлён файл конфигурации.",
    "affected_files": ["config.py"]
}
```

---

## Диаграмма взаимодействия

```mermaid
graph LR
    %% Определение стилей для различных типов узлов с улучшенной цветовой палитрой
    classDef clientStyle fill:#2c3e50, stroke:#1a252f, color:#ffffff, stroke-width:2px;
    classDef operationStyle fill:#8e44ad, stroke:#6c3483, color:#ffffff, stroke-width:2px;
    classDef systemStyle fill:#16a085, stroke:#117a65, color:#ffffff, stroke-width:2px;

    %% Узлы диаграммы
    A[Клиент]:::clientStyle

    subgraph Операции ПО
        B[Получение истории]:::operationStyle
        C[Запись изменения]:::operationStyle
    end

    subgraph Службы ОС
        D[Чтение и запись JSON]:::systemStyle
    end

    %% Связи между узлами
    A -->|GET /history/| B
    A -->|POST /history/| C

    B -->|Чтение файла истории| D
    C -->|Обновление файла истории| D

    D -->|Ответ клиенту| A
```

---

## Примечания
- История изменений сохраняется в файле `history_log.json`.
- Реализована обработка ошибок, таких как отсутствие файла или некорректные параметры запроса.
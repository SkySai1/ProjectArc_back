# Документация для приложения

Данный файл описывает основные компоненты приложения, их назначение и взаимодействие.

## Структура приложения

Приложение состоит из следующих основных компонентов:

### 1. **Маршруты (`routes`)**

**Описание:** Маршруты обрабатывают HTTP-запросы и предоставляют API для различных функций приложения.

- **Файлы (`files`)**: Управление файлами в проекте.
- **История (`history`)**: Логирование изменений и получение истории.
- **Политика конфиденциальности (`privacy`)**: Управление политикой конфиденциальности.
- **Карта проекта (`project_map`)**: Управление структурой проекта.
- **Описание (`about`)**: Управление общим описанием проекта.

Подробнее: [routes/README.md](routes/README.md)

### 2. **Модели (`models.py`)**

**Описание:** Определяет структуру базы данных и взаимодействие с ней через SQLAlchemy.

- Определение сущностей, таких как файлы и история изменений.
- Используется во всех маршрутах для работы с данными.

### 3. **Утилиты (`utils.py`)**

**Описание:** Вспомогательные функции для работы с базой данных, файлами и логированием.

- Обеспечивает повторно используемые функции для маршрутов.
- Минимизирует дублирование кода.

## Диаграмма компонентов приложения

```mermaid
graph TD
    %% Определение стилей для различных типов узлов
    classDef appStyle fill:#2c3e50, stroke:#1a252f, color:#ffffff, stroke-width:2px;
    classDef clientStyle fill:#43c910, stroke:#1a252f, color:#ffffff, stroke-width:2px;
    classDef routeStyle fill:#3498db, stroke:#2980b9, color:#ffffff, stroke-width:2px;
    classDef utilStyle fill:#8e44ad, stroke:#6c3483, color:#ffffff, stroke-width:2px;
    classDef modelStyle fill:#16a085, stroke:#117a65, color:#ffffff, stroke-width:2px;
    classDef systemStyle fill:#f39c12, stroke:#d68910, color:#ffffff, stroke-width:2px;
    classDef configStyle fill:#34495e, stroke:#2c3e50, color:#ffffff, stroke-width:2px;

    %% Узлы диаграммы
    A[Запросы клиента]:::clientStyle
    B[app/__init__.py]:::appStyle
    H[run.py Точка входа]:::appStyle
    I[config.py Настройки]:::configStyle

    subgraph Маршруты
        C[Маршруты API]:::routeStyle
        C1[About]:::routeStyle
        C2[Files]:::routeStyle
        C3[History]:::routeStyle
        C4[Privacy]:::routeStyle
        C5[Project Map]:::routeStyle
    end

    D[utils.py Утилиты]:::utilStyle
    E[models.py Модели]:::modelStyle

    subgraph Службы ОС
        F[База данных]:::systemStyle
        G[Файловая система]:::systemStyle
    end

    %% Связи между узлами
    A --> B
    B --> C
    C --> C1
    C --> C2
    C --> C3
    C --> C4
    C --> C5

    H --> B
    H <-.-> I

    C1 --> D
    C2 --> D
    C3 --> D
    C4 --> D
    C5 --> D

    D --> E
    E -->|Данные| F
    D -->|Операции| G

```

## Интеграция

Все компоненты приложения связаны через маршруты и общую базу данных. Это обеспечивает модульность и гибкость в расширении функциональности.

# Project Management API

This project provides a RESTful API for managing files, directories, and a project map. It is containerized using Docker and can be deployed with Docker Compose.

---

## Table of Contents

1. [Features](#features)
2. [Requirements](#requirements)
3. [Installation](#installation)
   - [Using Python](#using-python)
   - [Using Docker](#using-docker)
   - [Using Docker Compose](#using-docker-compose)
4. [API Endpoints](#api-endpoints)
   - [Create File](#1-create-file)
   - [Delete File or Directory (Update Project Map)](#2-delete-file-or-directory-update-project-map)
   - [Add or Update Entry in Project Map](#3-add-or-update-entry-in-project-map)
   - [Retrieve File Content](#4-retrieve-file-content)
   - [Retrieve Project Map](#5-retrieve-project-map)
   - [Update Project Map](#6-update-data-in-project-map)
   - [Delete data in Project map](#7-delete-data-from-project-map)
5. [Docker Setup](#docker-setup)
   - [Dockerfile](#dockerfile)
   - [Docker Compose](#docker-compose)
6. [Environment Variables](#environment-variables)
7. [License](#license)

---

## Features

- Create, update, delete files and directories.
- Maintain a structured project map in JSON format.
- Log changes to files and directories.
- Secure API access using an API key.

---

## Requirements

- Python 3.10+
- Flask
- Docker (optional for containerized deployment)

---

## Installation

### Using Python
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export PROJECT_DIR="project_data"
   export API_KEY="your_secret_key"
   ```

4. Run the application:
   ```bash
   python app.py
   ```

### Using Docker
1. Build the Docker image:
   ```bash
   docker build -t project_manager .
   ```

2. Run the Docker container:
   ```bash
   docker run -d -p 5000:5000 -e API_KEY=your_secret_key -e PROJECT_DIR=project_data project_manager
   ```

### Using Docker Compose
1. Update `compose.yaml` if needed (set `API_KEY` and `PROJECT_DIR`):
   ```yaml
   environment:
     - FLASK_ENV=development
     - API_KEY=your_secret_key
     - PROJECT_DIR=project_data
   ```

2. Start the services:
   ```bash
   docker-compose up -d
   ```

---

## API Endpoints

### 1. **Create File**
- **POST** `/create`
- **Description**: Creates a new file or directory and updates the project map.
- **Headers**: `Authorization: <API_KEY>`
- **Body**:
  ```json
  {
      "filename": "folder/subfolder/file.txt",
      "content": "File content here",
      "description": "Optional file description"
  }
  ```
- **Response**:
  - `201`: File created successfully.
  - `400`: Invalid request.
  - `401`: Unauthorized.

### 2. **Delete File or Directory (Update Project Map)**
- **POST** `/project_map`
- **Description**: Deletes a specific file or folder from the project map.
- **Headers**: `Authorization: <API_KEY>`
- **Body**:
  ```json
  {
      "path": "folder/subfolder/file.txt"
  }
  ```
- **Response**:
  - `200`: File or folder deleted successfully.
  - `404`: File or folder not found in the project map.
  - `500`: Error occurred while processing.

### 3. **Add or Update Entry in Project Map**
- **PUT** `/project_map`
- **Description**: Adds or updates an entry in the project map for a specific file.
- **Headers**: `Authorization: <API_KEY>`
- **Body**:
  ```json
  {
      "path": "folder/subfolder/file.txt",
      "description": "Updated description",
      "size": 1234,
      "last_modified": 1698765436
  }
  ```
- **Response**:
  - `200`: Entry added or updated successfully.
  - `400`: Invalid request.
  - `500`: Error occurred while processing.

### 4. **Retrieve File Content**
- **GET** `/get_file`
- **Description**: Retrieves the content of a specific file.
- **Headers**: `Authorization: <API_KEY>`
- **Query Parameters**:
  - `filename`: The path to the file.
- **Response**:
  ```json
  {
      "filename": "folder/subfolder/file.txt",
      "content": "File content here"
  }
  ```

### 5. **Retrieve Project Map**
- **GET** `/project_map`
- **Description**: Retrieves the current project map in JSON format.
- **Headers**: `Authorization: <API_KEY>`
- **Response**:
  ```json
  {
      "folder/subfolder": {
          "file.txt": {
              "description": "File description",
              "size": 123,
              "last_modified": 1698765436
          }
      }
  }
  ```

### 6. **Update data in project map**
- **Метод**: `PUT`
- **Описание**: Добавляет или обновляет информацию о конкретном файле в карте проекта.
- **Заголовки**: 
  - `Authorization: <API_KEY>`
- **Тело запроса**:
  ```json
  {
      "path": "folder/subfolder/file.txt",
      "description": "Description of the file",
      "size": 1234,
      "last_modified": 1698765436
  }
  ```
- **Ответы**:
  - `200`: Запись добавлена или обновлена успешно.
    ```json
    {
        "message": "File 'folder/subfolder/file.txt' successfully added or updated in the project map."
    }
    ```
  - `400`: Некорректный запрос (отсутствуют обязательные ключи или неверный формат данных).
  - `500`: Ошибка при обработке.


### 7. **Delete data from project map**
- **Метод**: `POST`
- **Описание**: Удаляет информацию о конкретном файле или папке из карты проекта.
- **Заголовки**: 
  - `Authorization: <API_KEY>`
- **Тело запроса**:
  ```json
  {
      "path": "folder/subfolder/file.txt"
  }
  ```
- **Ответы**:
  - `200`: Указанный путь успешно удалён из карты проекта.
    ```json
    {
        "message": "Path 'folder/subfolder/file.txt' deleted from project map."
    }
    ```
  - `404`: Указанный путь не найден в карте проекта.
  - `500`: Ошибка при обработке.

---

## Docker Setup

### Dockerfile
The `Dockerfile` is configured as follows:
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt requirements.txt
COPY app.py app.py
COPY utils.py utils.py
RUN mkdir files
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "app.py"]
```

### Docker Compose
The `compose.yaml` sets up the environment for the container:
```yaml
version: "3.9"
services:
  project_manager:
    image: gpt_storage
    container_name: gpt_storage
    ports:
      - "5001:5000"
    volumes:
      - ./blog_project:/app/blog_project
    environment:
      - FLASK_ENV=development
      - API_KEY=key
      - PROJECT_DIR=blog_project
```

---

## Environment Variables

| Variable      | Description                        | Default Value   |
|---------------|------------------------------------|-----------------|
| `PROJECT_DIR` | Directory to store files          | `project_data`  |
| `API_KEY`     | API key for secure access         | `default_secret_api_key` |

---

## License

This project is licensed under the MIT License.

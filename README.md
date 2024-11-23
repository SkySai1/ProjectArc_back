
# Project Manager API

Flask API for managing files and directories with support for creating, updating, and deleting files and folders. Includes authentication via API key.

---

## Table of Contents

- [Getting Started](#getting-started)
- [Endpoints](#endpoints)
  - [1. Create File](#1-create-file)
  - [2. Upload File](#2-upload-file)
  - [3. Edit File](#3-edit-file)
  - [4. Get Project Map](#4-get-project-map)
  - [5. Delete File or Folder](#5-delete-file-or-folder)
- [Environment Variables](#environment-variables)

---

## Getting Started

### Requirements

- Python 3.10+
- Docker (optional)
- Nginx (optional)

### Installation

1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Flask app:
   ```bash
   python app.py
   ```

---

## Endpoints

### 1. Create File

Creates a new file, including all missing folders.

- **URL:** `/create`
- **Method:** `POST`
- **Headers:**
  ```http
  Authorization: your_secret_api_key
  Content-Type: application/json
  ```
- **Body:**
  ```json
  {
      "filename": "folder/subfolder/example.py",
      "content": "print('Hello, world!')"
  }
  ```
- **Example with `curl`:**
  ```bash
  curl -X POST http://localhost:5000/create        -H "Authorization: your_secret_api_key"        -H "Content-Type: application/json"        -d '{"filename": "folder/subfolder/example.py", "content": "print(\"Hello, World!\")"}'
  ```

---

### 2. Upload File

Uploads an existing file.

- **URL:** `/upload`
- **Method:** `POST`
- **Headers:**
  ```http
  Authorization: your_secret_api_key
  ```
- **Body:** File sent as `form-data`.
- **Example with `curl`:**
  ```bash
  curl -X POST http://localhost:5000/upload        -H "Authorization: your_secret_api_key"        -F "file=@path_to_your_file"
  ```

---

### 3. Edit File

Updates the content of an existing file.

- **URL:** `/edit`
- **Method:** `POST`
- **Headers:**
  ```http
  Authorization: your_secret_api_key
  Content-Type: application/json
  ```
- **Body:**
  ```json
  {
      "filename": "folder/subfolder/example.py",
      "content": "print('Updated content!')"
  }
  ```
- **Example with `curl`:**
  ```bash
  curl -X POST http://localhost:5000/edit        -H "Authorization: your_secret_api_key"        -H "Content-Type: application/json"        -d '{"filename": "folder/subfolder/example.py", "content": "print(\"Updated content!\")"}'
  ```

---

### 4. Get Project Map

Retrieves the current project structure.

- **URL:** `/project_map`
- **Method:** `GET`
- **Headers:**
  ```http
  Authorization: your_secret_api_key
  ```
- **Example with `curl`:**
  ```bash
  curl -X GET http://localhost:5000/project_map        -H "Authorization: your_secret_api_key"
  ```

---

### 5. Delete File or Folder

Deletes a specified file or folder.

- **URL:** `/delete`
- **Method:** `DELETE`
- **Headers:**
  ```http
  Authorization: your_secret_api_key
  Content-Type: application/json
  ```
- **Body:**
  ```json
  {
      "path": "folder/subfolder/example.py"
  }
  ```
- **Example with `curl`:**
  ```bash
  curl -X DELETE http://localhost:5000/delete        -H "Authorization: your_secret_api_key"        -H "Content-Type: application/json"        -d '{"path": "folder/subfolder/example.py"}'
  ```

---

## Environment Variables

- **`API_KEY`**: Set the API key for authenticating requests. Use this variable in your environment or Docker setup.

---

## Running with Docker

1. Build the Docker image:
   ```bash
   docker build -t project_manager .
   ```

2. Run the container:
   ```bash
   docker run -d -p 5000:5000 --name project_manager         -e API_KEY=your_secret_api_key         -v $(pwd)/files:/app/files         -v $(pwd)/project_map.json:/app/project_map.json         project_manager
   ```

3. Access the application at `http://localhost:5000`.

---

## Notes

- Ensure `Authorization` headers are set for all requests.
- Adjust `client_max_body_size` in Nginx configuration if handling large files.

---
# project_storage

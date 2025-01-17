
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
   - [About API Documentation](app/routes/about/README.md)
   - [Files API Documentation](app/routes/files/README.md)
   - [History API Documentation](app/routes/history/README.md)
   - [Privacy API Documentation](app/routes/privacy/README.md)
   - [Project Map API Documentation](app/routes/project_map/README.md)
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

### [About API Documentation](data/app/routes/about/README.md)
- Provides information about managing project descriptions.

### [Files API Documentation](data/app/routes/files/README.md)
- Handles file creation, deletion, and updates.

### [History API Documentation](data/app/routes/history/README.md)
- Manages the logging and retrieval of project change history.

### [Privacy API Documentation](data/app/routes/privacy/README.md)
- Offers multi-language support for privacy policies.

### [Project Map API Documentation](data/app/routes/project_map/README.md)
- Facilitates managing and syncing the project map with the filesystem.

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

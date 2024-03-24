# ASL Fingerspelling Recognition

## Description

This project focuses on American Sign Language (ASL) fingerspelling recognition.

## Prerequisites

- Python 3.8
- Pip (Python package installer)
- Docker
- Docker Compose

## Installation

### Local Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/alostracco/ASL-Fingerspelling-Recognition.git
   cd ASL-Fingerspelling-Recognition
   ```

2. **Switch to the Backend Branch:**

   ```bash
   git checkout backend
   ```

3. **Create a Virtual Environment:**

   ```bash
   python3.8 -m venv venv
   ```

4. **Activate the Virtual Environment:**

   - On Windows:

     ```bash
     venv\Scripts\activate
     ```

   - On macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

5. **Install Requirements:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Run Server:**

   ```bash
   python manage.py runserver 8080
   ```

   This will start the server and you can access your app at `http://localhost:8080/`

### Docker Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/alostracco/ASL-Fingerspelling-Recognition.git
   cd ASL-Fingerspelling-Recognition
   ```

2. **Switch to the Backend Branch:**

   ```bash
   git checkout backend
   ```

3. **Build and Start Docker Containers:**

   Ensure you have Docker and Docker Compose installed on your system. Then, in the project root directory, run:

   ```bash
   docker-compose up --build
   ```

   This will build and start the server containers defined in the `docker-compose.yml` file, and you can access your app at `http://localhost:8080/`

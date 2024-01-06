# ASL Fingerspelling Recognition

## Description

This project focuses on American Sign Language (ASL) fingerspelling recognition.

## Prerequisites

- Python 3.8
- Pip (Python package installer)

## Installation

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

## Running the Server

Ensure you are in the project root directory and your virtual environment is activated.

```bash
python manage.py runserver
```

This will start the development server, and you can access your app at `http://localhost:8000/`.

# n8n-Driven Resume Analyzer

This project is a secure, containerized, AI-powered system that automates the process of parsing and analyzing PDF resumes. A user can upload a resume, which triggers a backend process to extract key information using an n8n workflow and store the structured data in a PostgreSQL database.

## Architecture

The system consists of the following services orchestrated by Docker Compose:

* **FastAPI Backend:** A Python backend that handles file uploads and triggers the n8n workflow.
* **n8n:** An automation platform that processes the resume, extracts information using Google Gemini, and inserts it into the database.
* **PostgreSQL:** A database to store the structured resume data.
* **pgAdmin:** A web-based administration tool for PostgreSQL.

## Prerequisites

* Docker
* Docker Compose

## Setup

1.  **Create the `.env` file:**

    Create a file named `.env` in the root of the project and add the following content. Replace the placeholder values with your actual credentials and secrets.

    ```env
    # .env

    # === n8n Configuration ===
    # The GOOGLE_AI_API_KEY for the Gemini model
    GOOGLE_AI_API_KEY=your_secret_gemini_api_key

    # === Backend Configuration ===
    # The full webhook URL for n8n. The service name 'n8n' is used, not 'localhost'.
    # IMPORTANT: The webhook ID must match the one in your production workflow in n8n.
    N8N_WEBHOOK_URL=http://n8n:5678/webhook/your-production-webhook-id

    # A secret key for JWT token generation
    JWT_SECRET_KEY=your-super-strong-secret-key-for-jwt

    # === Database Credentials ===
    # Used by Postgres, n8n, and pgAdmin services
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=mysecretpassword
    POSTGRES_DB=resume_analyzer_db

    # === pgAdmin Configuration ===
    # Login credentials for the pgAdmin web interface
    PGADMIN_DEFAULT_EMAIL=admin@example.com
    PGADMIN_DEFAULT_PASSWORD=admin
    ```

2.  **Place the n8n workflow:**

    Place your exported n8n workflow file at `n8n-data/workflows/resume_analyzer.json`.

## Running the Application

To start the entire application stack, run the following command from the project root:

```bash
docker-compose up -d
````

## Accessing the Services

  * **n8n UI:** [http://localhost:5678](https://www.google.com/search?q=http://localhost:5678)
  * **pgAdmin UI:** [http://localhost:5050](https://www.google.com/search?q=http://localhost:5050)
      * **Username:** `admin@example.com`
      * **Password:** `admin`
  * **Backend API:** [http://localhost:8000/docs](https://www.google.com/search?q=http://localhost:8000/docs)

## Project Structure

```
resume-analyzer/
├── backend/
│   ├── auth.py
│   ├── create_table.py
│   ├── Dockerfile
│   ├── main.py
│   ├── requirements.txt
│   └── upload.py
├── n8n-data/
│   └── workflows/
│       └── resume_analyzer.json
├── .env
├── docker-compose.yml
└── README.md
```
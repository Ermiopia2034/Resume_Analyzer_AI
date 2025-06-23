# n8n-Driven Resume Analyzer

This project is a secure, containerized, AI-powered system that automates the process of parsing and analyzing PDF resumes. It provides a secure API endpoint to upload a resume, which triggers an n8n workflow to extract key information and store it in a PostgreSQL database.

## Architecture

The system consists of the following services orchestrated by Docker Compose:

* **FastAPI Backend:** A Python backend that handles authentication, file uploads, and triggers the n8n workflow.
* **n8n:** An automation platform that processes the resume, extracts information using Google Gemini, and inserts it into the database.
* **PostgreSQL:** A database to store the structured resume data.
* **pgAdmin:** A web-based administration tool for PostgreSQL.
  
```mermaid
  sequenceDiagram
    participant Browser as User's Browser
    participant Backend as FastAPI Backend
    participant N8N as n8n Service
    participant Postgres as PostgreSQL DB
    participant Gemini as Google Gemini API

    Note over Browser, Gemini: 1. Authentication
    
    Browser->>+Backend: POST /auth/login<br/>(username, password)
    Note right of Backend: - Verifies credentials against hardcoded user.<br/>- Creates a JWT access token.
    Backend-->>-Browser: 200 OK<br/>{ "access_token": "...", "token_type": "bearer" }

    Note over Browser, Gemini: 2. Resume Upload and Processing
    
    Browser->>+Backend: POST /upload<br/>Header: Authorization: Bearer {token}<br/>Body: Multipart form with PDF file
    Note right of Backend: - Verifies the JWT is valid.<br/>- Receives the uploaded file.
    Backend->>+N8N: POST /webhook/a1b2c3d4...<br/>(Forwards PDF in a multipart form field named "file")
    Backend-->>-Browser: 200 OK<br/>{ "message": "File successfully uploaded..." }

    rect rgb(240, 248, 255)
        Note over N8N: n8n Workflow Execution
        N8N->>N8N: 1. Extract Text from File<br/>(Reads binary data from the "file" property)
        N8N->>+Gemini: 2. Call LLM<br/>(Sends extracted text with a prompt for JSON)
        Gemini-->>-N8N: 3. Return Structured Data<br/>(Response is a string containing a JSON object)
        N8N->>N8N: 4. Parse JSON<br/>(Code node cleans and parses the string from the LLM)
        N8N->>+Postgres: 5. INSERT INTO resumes (...)<br/>(Connects using "postgres" as hostname)
        Postgres-->>-N8N: 6. Confirm Write
    end
    
    N8N-->>-Backend: (No direct response - "Fire and Forget")
```

## Prerequisites

* Docker & Docker Compose
* `curl` or an API client like Postman for testing

## Setup

1.  **Clone the Repository:**
    ```sh
    git clone <repository-url>
    cd resume-analyzer
    ```

2.  **Review Environment Variables:**
    This project includes a pre-configured `.env` file for ease of testing. Please review this file to ensure the values are correct for your environment, especially your `GOOGLE_AI_API_KEY`.


## Running the Application

1.  **Start all services:**
    Run the following command from the project root to build and start the containers in detached mode.
    ```bash
    sudo docker compose up --build -d
    ```

2.  **Verify services are running:**
    ```bash
    sudo docker compose ps
    ```

## Usage & Testing

Since there is no frontend, you can test the API endpoints using `curl`.

1.  **Get an Authentication Token:**
    The backend uses a hardcoded user for authentication. Use the following command to get a JWT.
    ```sh
    curl -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/x-www-form-urlencoded" -d "username=testuser&password=testpassword"

    ```

2.  **Upload a Resume for Analysis:**
    With the token provided from the above command, you can now upload a PDF file to the secure endpoint. Replace `cv.pdf` with the actual resume PDF file and also make sure you are running this command from the directory where 'cv.pdf' is located.
    ```sh
    curl -X POST "http://localhost:8000/upload" -H "Authorization: Bearer YOURTOKENHERE" -F "file=@cv.pdf"

    ```
    On success, this will return `{"message": "File uploaded and sent to workflow successfully."}`.

3.  **Verify the Result in the Database:**
    - Navigate to the **pgAdmin UI** at `http://localhost:5050`.
    - Log in with the credentials from your `.env` file. (username: admin@example.com, password: admin)
    - Connect to the `resume_analyzer_db` and query the `resumes` table to see the newly inserted structured data.

## Accessing the Services

* **Backend API Docs:** `http://localhost:8000/docs`
* **n8n UI:** `http://localhost:5678`
* **pgAdmin UI:** `http://localhost:5050`
    * **Username:** as defined in `PGADMIN_DEFAULT_EMAIL`
    * **Password:** as defined in `PGADMIN_DEFAULT_PASSWORD`

## Project Structure

````

resume-analyzer/
├── backend/
│   ├── main.py
│   ├── auth.py
│   ├── upload.py
│   ├── requirements.txt
│   └── Dockerfile
├── n8n-data/
│   └── workflows/
│       └── resume\_analyzer.json
├── .env
├── docker-compose.yml
└── README.md

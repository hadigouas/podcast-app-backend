# Podcast App - Backend

This is the **FastAPI** backend for the Podcast App. It handles API requests, database operations, and audio file storage.

---

## Features

- **Podcast Upload API**: Upload podcasts with metadata and store audio files.
- **Search API**: Fetch and filter podcasts.
- **Database Management**: Store podcast data securely using PostgreSQL.

---

## Getting Started

### Prerequisites

- **Python** (3.10 or later)  
  [Install Python](https://www.python.org/downloads/)
- **PostgreSQL** (13 or later)  
  [Install PostgreSQL](https://www.postgresql.org/download/)

---

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/podcast-app.git
   cd podcast-app/backend
###Create a virtual environment:

python -m venv env
source env/bin/activate  # On Windows: .\env\Scripts\activate
###Install dependencies:

pip install -r requirements.txt
###Configure the database in config.py:

DATABASE_URL = "postgresql://username:password@localhost:5432/podcast_app"
###Run the server:

uvicorn main:app --reload

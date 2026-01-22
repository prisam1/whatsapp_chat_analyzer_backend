# WhatsApp Chat Analyzer - Backend (FastAPI)

This is the Python-based processing engine for the WhatsApp Chat Analyzer. It uses FastAPI to provide a high-performance REST API that parses raw chat exports using Regex.

## Features
- **Regex Parsing**: Efficiently extracts dates, times, and users from standard WhatsApp formats.
- **Asynchronous Processing**: Built on FastAPI for rapid file handling.
- **Data Insights**: Calculates unique daily active users and identifies "Power Users" (active 4+ days/week).

## Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/prisam1/whatsapp_chat_analyzer_backend.git](https://github.com/prisam1/whatsapp_chat_analyzer_backend.git)
   cd whatsapp_chat_analyzer_backend

2. **Create and activate Virtual Environment:**

python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

3. **Install Dependencies:**
pip install fastapi uvicorn python-multipart

4. **Run the Server:**

uvicorn main:app --reload

The backend will be live at http://localhost:8000.

## API Endpoints
POST /analyze: Accepts a .txt file and returns JSON data for charts and user lists.
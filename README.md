# VisionAI Pro

AI Powered Image Recognition Platform

## Features

- User Authentication
- Image Upload
- Image Classification
- Object Detection (YOLOv8)
- OCR (EasyOCR)
- Dashboard Analytics
- PDF Report Generation
- REST API
- Render Deployment

---

## Installation

### Clone Repository

```bash
git clone https://github.com/yourusername/visionai-pro.git

cd visionai-pro
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

```bash
cp .env.example .env
```

Update values inside:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///visionai.db
```

### Run Migrations

```bash
flask db init

flask db migrate -m "initial migration"

flask db upgrade
```

### Start Application

```bash
python app.py
```

Application URL:

```text
http://127.0.0.1:5000
```

---

## API Endpoints

### Health

```http
GET /api/health
```

### Classification

```http
POST /api/classify
```

### Detection

```http
POST /api/detect
```

### OCR

```http
POST /api/ocr
```

### Full Analysis

```http
POST /api/analyze
```

---

## Deployment

Push repository to GitHub.

Create new Render Web Service.

Build Command:

```bash
pip install -r requirements.txt
```

Start Command:

```bash
gunicorn wsgi:app
```

Add Environment Variables from `.env`.

Deploy.
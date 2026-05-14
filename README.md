# AI Platform

Multi-service application with Django backend and ML model services.

## Services

- **Backend**: Django REST API on port 8000
- **Feces Model**: Poultry disease detection on port 8001
- **Waste Model**: Trash detection on port 8002

## Quick Start

```bash
docker-compose up -d
```

Visit:
- Backend: http://localhost:8000
- Feces API: http://localhost:8001/docs
- Waste API: http://localhost:8002/docs

## Development

To run services individually:

```bash
# Backend
cd backend && python manage.py runserver

# Feces Model
cd feces_model && python -m uvicorn api:app --host 0.0.0.0 --port 8000

# Waste Model
cd waste_model && python -m uvicorn src.main:app --host 0.0.0.0 --port 8080
```
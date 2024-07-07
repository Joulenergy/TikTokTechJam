# Project CommentSense

## Getting Started

### 1. Setup a Gemini API (it's free!)
Register for an API key: https://ai.google.dev/
Setup the API key inside a .env file

```bash
cd backend/
touch .env
```

```.env
GOOGLE_API_KEY=<API-KEY-GOES-HERE>
```

### 2. Build the backend and frontend docker images
**Build the frontend docker image**
```bash
cd frontend/
docker build -t frontend .
```

**Build the backend docker image**
```bash
cd backend/
docker build -t server .
```

### 3. Run Docker Compose
```
docker-compose build
docker-compose up -d
```

## 
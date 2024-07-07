# Project CommentSense

## Requirements
- A CUDA Compatible GPU for Quantization

## Setup

### 1. Download the Llava-Next model by running the downloadModel.py script
```
pip install -r requirements.txt
python downloadModel.py
```

### 2. Setup a Gemini API (it's free!)
Register for an API key: https://ai.google.dev/
Setup the API key inside a .env file
```.env
GOOGLE_API_KEY=<API-KEY-GOES-HERE>
```

### 3. Build the backend and frontend docker images
**Build the frontend docker image**
```
cd frontend/
docker build -t frontend .
```

**Build the backend docker image**
```
cd backend/
docker build -t server .
docker run -d --name server --env-file .env  -p 8000:8000 server
```

### 4. Run Docker Compose
```
docker compose -d up
```
# Project CommentSense

CommentSense is an AI-powered content analysis and feedback system for TikTok videos. It leverages advanced natural language processing and computer vision technologies to provide creators with comprehensive insights and interactive assistance for their content.

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

### 2. Run Docker Compose
```
docker-compose build
docker-compose up -d
```

## Key Features
1. Automated Content Analysis: Users input a TikTok video URL, triggering a multi-step analysis process.

2. Comment Scraping and Clustering: The system extracts comments from the video and uses machine learning to categorize them into meaningful groups.
   
3. Video Context Extraction: Employing the LLaVA (Large Language and Vision Assistant) model, the application derives additional context from the video content itself.

4. Integrated Database Storage: All analyzed data is efficiently stored in a SQLite database for quick retrieval and persistent insights.

5. AI-Powered Interactive Assistant: An intelligent chatbot with agentic properties provides users with tailored feedback and answers based on the analyzed video context and user queries.

## Data Flow
1. User inputs TikTok URL in frontend
   
2. Backend receives URL and initiates scraping and analysis process
   
3. Scraped data passes through the processing pipeline
   
4. Processed data is stored in the SQLite database
   
5. User navigates to chat interface
   
6. Chat agent retrieves context from the database
   
7. User interacts with the chat agent, which provides responses based on the video context and user queries
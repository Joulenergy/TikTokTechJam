from typing import Union, Tuple, List, Optional
from pydantic import BaseModel

from fastapi import FastAPI


app = FastAPI()

class VideoContent(BaseModel):
    videoSummary: str
    videoContent: List[str] 

@app.get("/")
def home():
    return {"text": "Site is up!"}

@app.get("/videos/comments/{videoURL}")
def scrapeVideo(videoURL: str = ""):
    # TODO: Scrape Video Comments
    return {"text": [
        "This is a comment", "This is another comment", "Humours of Whiskey"
    ]}

@app.get("/videos/summarise/{videoURL}")
def summariseVideo(videoURL: str = ""):
    # TODO: Summarise video content using llava-next 
    return {"text": "Video Summary Description"} 

@app.post("/prompt") 
def promptLLM(videoContent: VideoContent): 
    # TODO: Extract video summary and list of comments from request body 
    # TODO: Prompt LLM 
    return {"text": "Response generated by LLM"}

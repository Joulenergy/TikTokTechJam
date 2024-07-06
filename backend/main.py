from typing import List, Dict
import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed
import json

from fastapi import Query, Body, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session  
from backend import app, get_db
from pydantic import BaseModel

from .ai_models import VideoSummary, CommentSummary
from .sql_app import crud, models, schemas


class VideoURLS(BaseModel):
    URLS: List[str]

@app.get("/")
def home():
    """
    API to check if the site is up
    """
    return {"text": "Site is up!"}

# Video endpoints
@app.post("/videos/", tags=["videos"])
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return JSONResponse(content=crud.create_video(db=db, video=video).__dict__)

@app.get("/videos/", tags=["videos"])
def read_videos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    videos = crud.get_videos(db, skip=skip, limit=limit)
    return JSONResponse(content={"videos": [video.__dict__ for video in videos]})

@app.get("/videos/{video_id}", tags=["videos"])
def read_video(video_id: int, db: Session = Depends(get_db)):
    db_video = crud.get_video(db, video_id=video_id)
    if db_video is None:
        return JSONResponse(status_code=404, content={"Error": "Video not found"})
    return JSONResponse(content=db_video.__dict__)

# Summarization endpoint
@app.post("/summarize/")
async def summarize_video_and_comments(
    videoURLS: VideoURLS = Body(
        ..., description="List of video URLs to scrape comments from"),
    db: Session = Depends(get_db)
):  
    if not videoURLS.URLS or len(videoURLS.URLS) == 0:
        return JSONResponse(status=422 ,content={"Error": "videoURLS cannot be empty"})

    results = {}

    for url in videoURLS.URLS:
        # Check if video exists in database
        db_video = db.query(models.Video).filter(models.Video.url == url).first()
        
        if db_video:
            # Video exists, retrieve comments
            comments = crud.get_video_comments_by_video(db, video_id=db_video.id)
            comment_dicts = []
            for comment in comments:
                summary = comment.__dict__["summary"]
                category_count = comment.__dict__["category_count"]
                comment_insights = json.loads(comment.__dict__["comment_insights"])
                representative_comments = json.loads(comment.__dict__["representative_comments"])
                comment_dict = {
                    "summary": summary,
                    "categoryCount": category_count,
                    "commentInsights": comment_insights,
                    "representativeComments": representative_comments
                }
                comment_dicts.append(comment_dict)
            results[url] = {
                "video_summary": db_video.summary,
                "title": db_video.title,
                "categories": {comment.comment_category: comment_dict for comment, comment_dict in zip(comments, comment_dicts)}
            }
        else:
            # Video doesn't exist, perform summarization
            # try:
            singleURLInput: VideoURLS = VideoURLS(URLS=[url])

            video_summary = {"results": {url: {"summary": "Video summary"}}}["results"][url]["summary"]


            data, err2 = summarize_comments_helper(threads=100, retries=3, scrapeCount=50, videoURLS=singleURLInput)
            print(data)
            if err2:
                results[url] = {"Error": data["Error"]}
                return JSONResponse(status=422, content=results)
            else:
                comment_summaries = data["results"][url]['categories']
                title = data["results"][url]['title']
            print(comment_summaries)
            
            # Store results in database
            new_video = crud.create_video(db, schemas.VideoCreate(
                url=url,
                title=title,
                summary=video_summary
            ))
            
            stored_comments = []
            for comment_category, comment_summary in comment_summaries.items():
                print(comment_category, comment_summary)
                stored_comment = crud.create_video_comment(db, schemas.VideoCommentCreate(
                    video_id=new_video.id,
                    comment_category=comment_category,
                    summary=comment_summary["summary"],
                    category_count=comment_summary["categoryCount"],
                    comment_insights=json.dumps(comment_summary.get("commentInsights", [''])),
                    representative_comments=json.dumps(comment_summary.get("representativeComments", [''])),
                ))
                stored_comments.append(stored_comment.__dict__)
            
            results[url] = {
                "video_summary": video_summary,
                "title": title,
                "categories": comment_summaries
            }

    return JSONResponse(content={"results": results})


@app.post("/summarize/comments/")
def summarize_comments(
    threads: int = Query(100, description="Number of threads to use for scraping"),
    retries: int = Query(3, description="Number of retries for each video URL"),
    scrapeCount: int = Query(
        50, description="Number of comments to scrape per request"),
    videoURLS: VideoURLS = Body(
        ..., description="List of video URLs to scrape comments from")
    ) -> JSONResponse:
    """
    API to scrape comments from a list of video URLs scraping approximately 150±50 comments per second

    Returns a JSON object with the video URL as the key and a dictionary of comments as the value

    Args:

    - threads (int): Number of threads to use for scraping

    - retries (int): Number of retries for each video URL

    - scrapeCount (int): Number of comments to scrape per request

    - videoURLS (list[str]): List of video URLs to scrape comments from

    """
    commentsummarizer: CommentSummary = CommentSummary()
    if not videoURLS.URLS or len(videoURLS.URLS) == 0:
        return JSONResponse(status=422 ,content={"Error": "videoURLS cannot be empty"})

    results: dict = {}
    summaries: dict = {}

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(scrapeManager, link, scrapeCount, retries)
            for link in videoURLS.URLS
        ]

        for future in futures:
            result: Dict[str, List[str]] = future.result()
            results.update(result)

    for key, value in results.items():
        summaries[key] = commentsummarizer.get_comments_summary(value["comments"])
        # Add title
        summaries[key]["title"] = value["comments"][0]["title"]
        
    return JSONResponse(content={"results": summaries})


@app.post("/summarize/videos/")
async def summarize_video(
    threads: int = Query(100, description="Number of threads to use for summarisation"),
    videoURLS: VideoURLS = Body(
        ..., description="List of video URLs to scrape comments from")
    ) -> JSONResponse:
    """
API to get summary of a video from a list of video URLS

Returns a JSON object with the video URL as the key and a string of the summary

Args:

- threads (int): Number of threads to use for summarisation

- videoURLS (list[str]): List of video URLs to get video summaries from
"""
    videosummarizer: VideoSummary = VideoSummary()

    if not videoURLS.URLS or len(videoURLS.URLS) == 0:
        return JSONResponse(status=422 ,content={"Error": "videoURLS cannot be empty"})

    results = {}

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(videosummarizer.get_video_summary, link)
            for link in videoURLS.URLS
        ]

        for future in futures:
            result: Dict[str, List[str]] = future.result()
            results.update(result)

    return JSONResponse(content={"result": results})


@app.post("/prompt")
def promptLLM():
    # TODO: Extract video summary and list of comments from request body
    # TODO: Prompt LLM
    return {"text": "Response generated by LLM"}


# Helper Functions

########## Scrape Comments #############
def scrapeHandler(
    awemeID: str, scrapeCount: int, curr: int
) -> tuple[list[str], bool, bool]:
    url = f"https://www.tiktok.com/api/comment/list/?aweme_id={awemeID}&count={scrapeCount}&cursor={curr}"
    payload = {}
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9",
        "dnt": "1",
        "priority": "u=1, i",
        "sec-ch-ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    }

    try:
        response = requests.get(url, headers=headers, data=payload)
        response.raise_for_status()  # Raise an HTTPError for bad responses)
        data_json = response.json()

        # Check if the necessary keys are in the response
        if data_json and "comments" in data_json and "has_more" in data_json:
            data = [{"title": comment["share_info"]["title"] ,"text": comment["text"], "likes": comment["digg_count"]} for comment in data_json["comments"] if comment.get("comment_language") == "en"]
            has_more = bool(data_json["has_more"])
            return data, has_more, False
        else:
            print(f"Unexpected response format: {data_json}")
            # Write the response to a file for debugging
            return None, False, True

    except Exception as e:
        print(f"Error in scrapeHandler: {e}")
        return None, False, True

def scrapeManager(
    videoLink: str, scrapeCount: int, retryCount: int
) -> Dict[str, List[str]]:
    aweme_id = re.search(r"video\/([0-9]*)", videoLink)
    if aweme_id is None:
        print(f"Invalid video link: {videoLink}")
        return {videoLink: {"comments": [], "comment_count": 0, "error": "Invalid video link"}}

    aweme_id = aweme_id.group(1)
    comments = []
    retries = 0
    curr = 0
    has_more = True

    while has_more and retries < retryCount:
        data, has_more, err = scrapeHandler(aweme_id, scrapeCount, curr)
        if err:
            print(f"Retry {retries + 1}/{retryCount} for video {videoLink}")
            retries += 1
            continue
        else:
            comments.extend(data)
            curr += scrapeCount
            retries = 0

    # Sort comments by digg_count in descending order and take the top 100
    sorted_comments = sorted(comments, key=lambda x: x["likes"], reverse=True)[:250]

    return {videoLink: {"comments": sorted_comments, "comment_count": len(sorted_comments)}}

def summarize_video_helper(
    videoURLS: VideoURLS,
    threads: int = 100,
    ) -> JSONResponse:

    
        

def summarize_comments_helper(
    videoURLS: VideoURLS,
    threads: int = 100, 
    retries: int = 3, 
    scrapeCount: int = 50, 
    ) -> JSONResponse:

    commentsummarizer: CommentSummary = CommentSummary()

    if not videoURLS.URLS or len(videoURLS.URLS) == 0:
        return ({"Error": "videoURLS cannot be empty"}, True)

    results: dict = {}
    summaries: dict = {}

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(scrapeManager, link, scrapeCount, retries)
            for link in videoURLS.URLS
        ]

        for future in futures:
            result: Dict[str, List[str]] = future.result()
            results.update(result)

    for key, value in results.items():
        summaries[key] = commentsummarizer.get_comments_summary(value["comments"])
        # Add title
        summaries[key]["title"] = value["comments"][0]["title"]
        
    return ({"results": summaries}, False)
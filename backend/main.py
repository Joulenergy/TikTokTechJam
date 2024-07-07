from typing import List, Dict
import requests
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

from fastapi import Query, Body
from fastapi.responses import JSONResponse
from backend import app
from pydantic import BaseModel

from .models import VideoSummary, CommentSummary, PromptResponse

class VideoURLS(BaseModel):
    URLS: List[str]

class VideoSummaryInput(BaseModel):
    videoLink: str
    summary: str

class CommentsSummaryInput(BaseModel):
    videoLink: str
    commentSummary: str

class ChatPrompt(BaseModel):
    videoSummary: List[VideoSummaryInput]
    comments: List[CommentsSummaryInput]
    prompt: str

@app.get("/")
def home():
    """
    API to check if the site is up
    """
    return {"text": "Site is up!"}


@app.post("/summarise/comments/")
def summarise_comments(
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
    commentSummariser: CommentSummary = CommentSummary()
    if len(videoURLS.URLS) == 0:
        return JSONResponse(status=422, content={"Error": "videoURLS cannot be empty"})

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

    # Replace all single quotes with double quotes to avoid JSON parsing issues
    

    for key, value in results.items():
        summaries[key] = commentSummariser.get_comments_summary(value["comments"])
        
    return JSONResponse(content={"results": summaries})


@app.post("/summarise/videos/")
async def summarise_video(
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
    videoSummariser: VideoSummary = VideoSummary()

    if len(videoURLS.URLS)==0:
        return JSONResponse(status=422 ,content={"Error": "videoURLS cannot be empty"})

    results = {}

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [
            executor.submit(videoSummariser.get_video_summary, link)
            for link in videoURLS.URLS
        ]

        for future in futures:
            result: Dict[str, List[str]] = future.result()
            results.update(result)

    return JSONResponse(content={"result": results})


@app.post("/prompt")
def promptLLM(
    requestBody: ChatPrompt = Body(..., description="Request Body, requires videoSummary list[VideoSummaryInput], comments list[CommentsSummaryInput], prompt (str)")
    ) -> JSONResponse:

    promptResponse: PromptResponse = PromptResponse()

    userPrompt = requestBody.prompt
    videoSummary = requestBody.videoSummary
    commentSummary = requestBody.comments

    videoSummary = ''.join([video.videoLink + "\n" + video.summary for video in videoSummary])
    commentSummary = ''.join([video.videoLink + "\n" + video.commentSummary for video in commentSummary])

    response = promptResponse.get_prompt_response(commentSummary, videoSummary, userPrompt)
    # TODO: Extract video summary and list of comments from request body
    # TODO: Prompt LLM
    return JSONResponse(content={"response": response})


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
            data = [{"text": comment["text"], "likes": comment["digg_count"]} for comment in data_json["comments"] if comment.get("comment_language") == "en"]
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
    sorted_comments = sorted(comments, key=lambda x: x["likes"], reverse=True)[:100]

    print(sorted_comments)

    return {videoLink: {"comments": sorted_comments, "comment_count": len(sorted_comments)}}


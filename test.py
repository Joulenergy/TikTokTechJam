import requests

# Define the URL of the FastAPI endpoint
url = "http://127.0.0.1:8000/videos/comments/"

# Define the payload with video URLs
payload = {
    "URLS": [
        "https://www.tiktok.com/@youcureofficial/video/7363477383309053226",
        "https://www.tiktok.com/@blogilates/video/7118207082913942826",
        "https://www.tiktok.com/@blogilates/video/7370460897103449386",
        "https://www.tiktok.com/@youcureofficial/video/7384306298176785707",
        "https://www.tiktok.com/@naraazizasmith/video/7382679252577029422"
    ]
}

# Define the query parameters
params = {
    "threads": 10,
    "retries": 3,
    "scrapeCount": 50
}

# Make a POST request to the endpoint
response = requests.post(url, json=payload, params=params)

# Print the response
print(response.status_code)

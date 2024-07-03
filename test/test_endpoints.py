import pytest

# Unit Testing for endpoints
@pytest.mark.parametrize('urls',  
    [
        "https://www.tiktok.com/@youcureofficial/video/7363477383309053226",
        "https://www.tiktok.com/@blogilates/video/7118207082913942826",
        "https://www.tiktok.com/@naraazizasmith/video/7382679252577029422",
        "https://www.tiktok.com/@blogilates/video/7370460897103449386",
        "https://www.tiktok.com/@youcureofficial/video/7384306298176785707",
    ])
def test_scrape_comments(client, urls, capsys):
    endpoint = "/videos/comments/"

    with capsys.disabled():
        payload = {"URLS": [urls]}
        params = {"threads": 100, "retries": 3, "scrapeCount": 50}

        response = client.post(endpoint, json=payload, params=params)

        assert response.status_code == 200
        # Make sure that the payload is part of the response
        assert urls in response.json()['result']
        # Make sure response JSON is in the expected format
        assert 'comments' in response.json()['result'][urls]
        print(response.json()['result'][urls]['comments'])
        assert 'comment_count' in response.json()['result'][urls]

@pytest.mark.parametrize('urls',  
    [
        "https://www.tiktok.com/@youcureofficial/video/7363477383309053226",
        "https://www.tiktok.com/@blogilates/video/7118207082913942826",
        "https://www.tiktok.com/@naraazizasmith/video/7382679252577029422",
        "https://www.tiktok.com/@blogilates/video/7370460897103449386",
        "https://www.tiktok.com/@youcureofficial/video/7384306298176785707",
    ])
def test_summarise_videos(client, urls, capsys):
    endpoint = "/videos/summarise/"

    with capsys.disabled():
        payload = {"URLS": [urls]}

        response = client.post(endpoint, json=payload)

        assert response.status_code == 200
        # Make sure that the payload is part of the response
        assert urls in response.json()['result']
        print(response.json()['result'][urls]['summary'])
        # Make sure response JSON is in the expected format
        assert 'summary' in response.json()['result'][urls]



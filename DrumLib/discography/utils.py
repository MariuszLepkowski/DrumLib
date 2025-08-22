from urllib.parse import urlparse, parse_qs


def get_video_id(url):
    url_data = urlparse(url)
    query = parse_qs(url_data.query)
    video_id = query.get("v", [None])[0]
    return video_id


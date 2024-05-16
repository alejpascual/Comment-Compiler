import sys
import re
from googleapiclient.discovery import build
import instaloader
from TikTokApi import TikTokApi

def get_youtube_comments(video_url):
    API_KEY = 'AIzaSyCDEVTAtUCzkarKc_i3vd-BhdszUBo9kpg'
    # Enhanced regex pattern to match more YouTube URL formats
    video_id_match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})[^0-9A-Za-z_-]?", video_url)
    if not video_id_match:
        return "Invalid YouTube video URL"
    video_id = video_id_match.group(1)
    service = build('youtube', 'v3', developerKey=API_KEY)
    comments = []
    try:
        results = service.commentThreads().list(part='snippet', videoId=video_id, textFormat='plainText').execute()
        while results:
            for item in results['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)
            if 'nextPageToken' in results:
                results = service.commentThreads().list(part='snippet', videoId=video_id, textFormat='plainText', pageToken=results['nextPageToken']).execute()
            else:
                break
    except Exception as e:
        return f"Error fetching comments: {str(e)}"
    return comments

def get_instagram_comments(post_url):
    L = instaloader.Instaloader()
    shortcode = post_url.split('/')[-2]
    post = instaloader.Post.from_shortcode(L.context, shortcode)
    comments = [comment.text for comment in post.get_comments()]
    return comments

def get_tiktok_comments(video_url):
    api = TikTokApi.get_instance()
    video_id = video_url.split('/')[-1]
    comments = api.get_video_comments(video_id)
    return [comment['text'] for comment in comments]

def main(video_url):
    if 'youtube.com' in video_url or 'youtu.be' in video_url:
        return get_youtube_comments(video_url)
    elif 'instagram.com' in video_url:
        return get_instagram_comments(video_url)
    elif 'tiktok.com' in video_url:
        return get_tiktok_comments(video_url)
    else:
        return "Unsupported URL"

if __name__ == '__main__':
    if len(sys.argv) > 1:
        video_url = sys.argv[1]
    else:
        video_url = input("Enter the video URL: ")
    comments = main(video_url)
    if isinstance(comments, list):
        print('\n'.join(comments))
    else:
        print(comments)


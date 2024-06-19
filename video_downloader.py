import requests
import os

# Your RapidAPI key
api_key = "4f61715613mshe8fdda64d6aac61p10df3bjsna58bc62b0252"

# The URL of the TikTok video you want to download
tiktok_url = "https://vt.tiktok.com/ZSYfWCrEf/"

# The endpoint and headers for the API request
api_url = "https://tiktok-video-no-watermark2.p.rapidapi.com/"
headers = {
    "x-rapidapi-host": "tiktok-video-no-watermark2.p.rapidapi.com",
    "x-rapidapi-key": api_key
}

# The form data to be sent in the POST request
data = {
    "url": tiktok_url,
    "hd": "1"
}

# Make the POST request
response = requests.post(api_url, headers=headers, files=data)
response_data = response.json()

# Extract the video URL from the response
video_url = response_data['data']['play']

# Download the video
video_response = requests.get(video_url)

# Save the video to a file
video_filename = "tiktok_video.mp4"
with open(video_filename, 'wb') as f:
    f.write(video_response.content)

print(f"Video downloaded and saved as {video_filename}")

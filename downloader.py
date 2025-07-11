import yt_dlp
import os

def download_instagram_video(url: str, output_dir="downloads") -> tuple[str, str, str, str, str]:
    """
    Downloads the Instagram video and extracts the caption.

    Returns:
        (video_filepath, caption_text)
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),  # Save as downloads/UNIQUEID.mp4
        "cookiefile": "www.instagram.com_cookies.txt",  # 👈 This is the magic line
        "quiet": True,  # Suppress verbose output
    }

    # Use yt-dlp to download and extract info
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info is not None:
            caption = info.get("description", "")
            file_ext = info.get("ext", "mp4")
            video_id = info.get("id", "video")
            filename = os.path.join(output_dir, f"{video_id}.{file_ext}")
            Instagram_user = info.get("uploader", "Instagram User") # Optional: Get the uploader's name
            Instagram_id = info.get("uploader_id", "Instagram ID") # Optional: Get the uploader's ID
            Instagram_url = info.get("webpage_url", "https://www.instagram.com/")
            return filename, caption, Instagram_user, Instagram_id, Instagram_url
        else:
            return "", "", "", "", ""  # Return empty strings if extraction fails
        

def download_youtube_video(url: str, output_dir="downloads") -> tuple[str, str, str, str, str]:
    """
    Downloads the YouTube video and extracts the title.

    Returns:
        (video_filepath, title)
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Configure yt-dlp options
    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(output_dir, "%(id)s.%(ext)s"),  # Save as downloads/UNIQUEID.mp4
        "quiet": True,  # Suppress verbose output
    }

    # Use yt-dlp to download and extract info
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        if info is not None:
            title = info.get("title", "No Title")
            file_ext = info.get("ext", "mp4")
            video_id = info.get("id", "video")
            filename = os.path.join(output_dir, f"{video_id}.{file_ext}")
            youtube_user = info.get("uploader", "YouTube User")  # Optional: Get the uploader's name
            youtube_id = info.get("uploader_id", "YouTube ID")  # Optional: Get the uploader's ID
            # youtube_url = info.get("webpage_url", "https://www.youtube.com/")
            caption = info.get("description", "")
            return filename, title, youtube_user, youtube_id, caption
        else:
            return "", "", "", "", ""  # Return empty strings if extraction fails

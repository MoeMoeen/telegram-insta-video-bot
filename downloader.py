import yt_dlp
import os

def download_instagram_video(url: str, output_dir="downloads") -> tuple[str, str]:
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
            return filename, caption
        else:
            return "", ""

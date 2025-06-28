from downloader import download_instagram_video

url = "https://www.instagram.com/reel/DLVud_JBj7O/?igsh=bTY2dnVua3owdzg="  # Replace with a valid public URL

video_path, caption = download_instagram_video(url)

print(f"✅ Video downloaded to: {video_path}")
print(f"📝 Caption:\n{caption}")


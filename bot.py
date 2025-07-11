from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

import os
import re
from dotenv import load_dotenv

from downloader import download_instagram_video, download_youtube_video

load_dotenv()  # Load environment variables from .env file

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
if TELEGRAM_BOT_TOKEN is None:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message:
        await update.message.reply_text("👋 Hi! Send me an Instagram post URL and I'll fetch the video for you!")

# Echo handler for any message
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message and update.message.text:
        user_message = update.message.text.strip()
        # Check if the message is a valid Instagram post URL or YouTube video URL
        if is_instagram_post_url(user_message):
            await update.message.reply_text("📸 Processing your Instagram post URL...")
            
            try:
                video_filepath, caption, instagram_user, instagram_id, instagram_url = download_instagram_video(user_message)
                
                if not caption:
                    caption = "No caption available for this post."
                
                if video_filepath:
                    with open(video_filepath, 'rb') as video_file:
                        await update.message.reply_video(video_file, caption=caption[:1024])  # Limit caption to 1024 characters
                    await update.message.reply_text(f"Caption: {caption}\n\nInstagram User: {instagram_user}\nInstagram ID: {instagram_id}\nInstagram URL: {instagram_url}")

                    # os.remove(video_filepath)  # Clean up the downloaded file
                else:
                    await update.message.reply_text("❗️ Failed to download the video. Please try again later.")
            except Exception as e:
                await update.message.reply_text(f"❗️ An error occurred: {str(e)}")

        elif is_youtube_video_url(user_message):
            await update.message.reply_text("Processing your YouTube video URL...")
            
            try:
                filename, title, youtube_user, youtube_id, caption = download_youtube_video(user_message)

                if not title:
                    title = "No title available for this video."

                if filename:
                    with open(filename, 'rb') as video_file:
                        await update.message.reply_video(video_file, caption=title[:1024])  # Limit caption to 1024 characters
                    await update.message.reply_text(f"Title: {title}\n\nYouTube User: {youtube_user}\nYouTube ID: {youtube_id}\nCaption: {caption}")

                else:
                    await update.message.reply_text("❗️ Failed to download the video. Please try again later.")
            except Exception as e:
                await update.message.reply_text(f"❗️ An error occurred: {str(e)}")

        else:
            await update.message.reply_text("❗️ Please send a valid Instagram or YouTube post URL.")


def is_instagram_post_url(text: str) -> bool:
    """
    Checks if the text contains a valid Instagram post URL.
    """
    pattern = r"(https?://)?(www\.)?instagram\.com/(p|reel)/[A-Za-z0-9_\-]+/?"
    return re.search(pattern, text) is not None

def is_youtube_video_url(text: str) -> bool:
    """
    Checks if the text contains a valid YouTube video URL. Valid formats include:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/watch?v=VIDEO_ID
    - https://www.youtube.com/embed/VIDEO_ID
    - https://youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID
    - https://youtube.com/v/VIDEO_ID
    - https://www.youtube.com/shorts/VIDEO_ID
    - https://youtube.com/shorts/VIDEO_ID
    - https://www.youtube.com/live/VIDEO_ID
    - https://youtube.com/live/VIDEO_ID
    """
    pattern = r"(https?://)?(www\.)?(youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/shorts/|youtube\.com/live/)[A-Za-z0-9_\-]+"
    return re.search(pattern, text) is not None


# Main bot setup
if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    print("🤖 Bot is running...")
    app.run_polling()
import telebot
import pytube
import os
from googleapiclient.discovery import build
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from pytube import exceptions
from config import TOKEN_TELEGRAM
from config import YOUTUBE_API_KEY

bot = telebot.TeleBot(token=TOKEN_TELEGRAM)
API_KEY = YOUTUBE_API_KEY
youtube = build('youtube', 'v3', developerKey=API_KEY)


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, 'Hello! I am ready to help you find a video on a topic of interest on YouTube.')

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Looking for a video on YouTube at the request of the user
    search_response = youtube.search().list(
        q=message.text,
        type='video',
        part='id,snippet',
        maxResults=10
    ).execute()

    # Sort the results by statistics (views + likes)
    sorted_videos = sorted(search_response['items'], key=lambda x: (x.get('statistics', {'viewCount': 0, 'likeCount': 0})['viewCount'] + x.get('statistics', {'viewCount': 0, 'likeCount': 0})['likeCount']), reverse=True)

    # Get links to videos with the highest statistics
    best_video_links = [f"https://www.youtube.com/watch?v={video['id']['videoId']}" for video in sorted_videos[:3]]

    # Create button objects for each video
    download_buttons = [InlineKeyboardButton(text=f"Download video {i+1}", callback_data=video['id']['videoId']) for i, video in enumerate(sorted_videos[:3])]

    # Create a Markup Object and Add Buttons
    keyboard = InlineKeyboardMarkup().add(*download_buttons)

    # Adding a back button
    back_button = InlineKeyboardButton(text="Back", callback_data="back")
    keyboard.add(back_button)

    # Forming a message with links to videos
    message_text = "Here are the top results for your search:\n\n"
    for i, link in enumerate(best_video_links):
        message_text += f"{i+1}. {link}\n"

    # Send the user a message with links to the video and download buttons
    bot.send_message(chat_id=message.chat.id, text=message_text, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    if call.data == "back":
        # Redirecting the user back to the /start command
        bot.send_message(chat_id=call.message.chat.id, text="What else do you want to find?")
    else:
        # Getting the video ID from the callback request
        video_id = call.data

        # Creating a YouTube Video Object and uploading a video
        youtube_video = pytube.YouTube(f"https://www.youtube.com/watch?v={video_id}")
        video_file = None

        # Download a video with a long timeout
        for stream in youtube_video.streams:
            try:
                video_file = stream.download(timeout=1800)  # 30 minutes timeout
                break
            except pytube.exceptions.HTTPError:
                pass

        if video_file is None:
            # If none of the streams were successfully downloaded, raise an exception
            raise pytube.exceptions.VideoUnavailable("Unable to download the video")

        # Send the video to chat
        with open(video_file, 'rb') as video:
            bot.send_video(chat_id=call.message.chat.id, video=video)

        # Delete the video file
        os.remove(video_file)


if __name__ == '__main__':
    bot.polling(none_stop=True)
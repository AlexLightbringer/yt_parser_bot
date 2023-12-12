# YouTube Search and Download Telegram Bot

This Telegram bot allows users to search for YouTube videos based on their interests and download the top results. The bot utilizes the Telebot library for Telegram integration and the Pytube library for YouTube video downloads.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following dependencies installed:

- Python 3.x
- Telebot (`pip install pyTelegramBotAPI`)
- Pytube (`pip install pytube`)
- Google API Client (`pip install google-api-python-client`)

### Configuration

1. Obtain a Telegram Bot Token from the [BotFather](https://core.telegram.org/bots#botfather) and a YouTube API Key from the [Google Cloud Console](https://console.developers.google.com/).
2. Create a `.env` file and add your API keys there

### Running the Bot

Run the bot script by executing the following command:

```bash
python your_bot.py
```

## Usage

1. Start a chat with the bot on Telegram by sending the `/start` command.
2. Enter a search query, and the bot will fetch the top 3 results based on statistics (views + likes).
3. Receive a message with links to the top videos and download buttons.
4. Click the "Download" buttons to download the selected video.

## Features

- **Search YouTube**: Enter a query to search for relevant YouTube videos.
- **Download Videos**: Download the selected video with the click of a button.
- **Top Results**: Get the top 3 videos based on statistics (views + likes).
- **User-Friendly Interface**: Simple and intuitive interaction using Telegram chat.

## Callbacks

- **Back Button**: Return to the main menu by clicking the "Back" button.

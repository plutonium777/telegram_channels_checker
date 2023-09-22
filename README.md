# Telegram Channels Checker

![GitHub License](https://img.shields.io/badge/license-MIT-blue.svg)

A simple Python tool to check a list of Telegram channels, providing essential information such as channel title, validity, open/closed status, and member count.

## Features
- Check the status of multiple Telegram channels in one go.
- Quickly identify if a channel is open or closed.
- Get valuable insights into channel membership statistics.
- Easy-to-use with a straightforward text file input.

## Usage
1. Prepare a text file containing a list of Telegram channel links, one link per line.
2. Add some accounts in ./data/ folder.
3. Run the script, providing the path to the text file as input.
4. The script will process each channel link and display relevant information.

## Installation
1. Clone this repository:

   ```shell
   git clone https://github.com/plutonium777/telegram_channels_checker.git
2. Change directory:
   ```shell
   cd telegram_channels_checker
3. Install requirements:
   ```shell
   py -m pip install -r requirements.txt
4. Run
   ```shell
   py telegram_checker.py

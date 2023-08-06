# Telegram Notifier
This package provides simple notifications usable in python and shell programs
## Preparation:
- Create bot with BotFather and copy the `token`
- Send any message to the bot (needed to automatically get `chat_id`)
- install module:
```bash
pip install telegram-shell-notifier
```
## Usage:

```
telegram-notify [-h] [--token TOKEN] [--chat-id CHAT_ID] [--parse-mode PARSE_MODE] [FILE]

Notify user with a telegram message.

positional arguments:
  FILE                  File to read from, leave blank for reading from stdin.

optional arguments:
  -h, --help            show this help message and exit
  --token TOKEN         Token of the telegram bot, leave blank for environment variable.
  --chat-id CHAT_ID     Chat id, leave blank for environment variable.
  --parse-mode PARSE_MODE
                        Parse mode, passed directly to telegram bot api. Leave blank for HTMLIt can be Markdown, MarkdownV2, HTML
```

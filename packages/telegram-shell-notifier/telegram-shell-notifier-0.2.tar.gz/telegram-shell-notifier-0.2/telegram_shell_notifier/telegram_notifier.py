#!/usr/bin/env python
import requests


class TelegramNotifier:
    def __init__(self, token: str, chat_id: str, parse_mode: str = None):
        if token is None:
            raise ValueError("Can't convert None to str")
        if type(chat_id) is not int:
            chat_id = int(chat_id)
        self._token = token
        self._parse_mode = parse_mode
        self._chat_id = chat_id

    def send(self, msg: str):
        data = {
            "chat_id": self._chat_id,
            "text": msg
        }
        if self._parse_mode:
            data["parse_mode"] = self._parse_mode
        try:
            response = requests.get(f"https://api.telegram.org/bot{self._token}/sendMessage", data=data, timeout=10)
            if response.status_code != 200 or response.json()["ok"] is not True:
                print(f"Failed to send notification:\n\tstatus_code={response.status_code}\n\tjson:\n\t{response.json()}")
        except Exception as e:
            print(f"Failed to send notification:\n\texception:\n\t{e}")


def main():
    from os import environ
    from argparse import ArgumentParser

    arg_parser = ArgumentParser(prog="telegram-notify",
                                description="Notify user with a telegram message.")
    arg_parser.add_argument("--token", help="Token of the telegram bot, leave blank for environment variable.")
    arg_parser.add_argument("--chat-id", help="Chat id, leave blank for environment variable.")
    arg_parser.add_argument("--parse-mode", help="Parse mode, passed directly to telegram bot api. Leave blank for HTML"
                                                 "It can be Markdown, MarkdownV2, HTML")
    arg_parser.add_argument("file", metavar="FILE", nargs="?", help="File to read from, blank for stdin.", default=None)

    args = arg_parser.parse_args()

    token = args.token
    if token is None:
        token = environ.get("TELEGRAM_TOKEN")
    if token is None:
        arg_parser.error("Can't retrieve telegram token")

    chat_id = args.chat_id
    if chat_id is None:
        chat_id = environ.get("TELEGRAM_CHAT_ID")
    if chat_id is None:
        arg_parser.error("Can't retrieve telegram chat id")

    parse_mode = args.parse_mode
    if parse_mode is None:
        parse_mode = "HTML"

    f = None
    try:
        if args.file is None:
            from select import select
            from sys import stdin as f
        else:
            import os.path

            try:
                os.open(args.file, os.O_RDONLY)
            except FileNotFoundError:
                arg_parser.error("File not found")
            f = open(args.file)
        body = f.read()
    finally:
        if f is not None:
            f.close()

    notifier = TelegramNotifier(token, parse_mode=parse_mode, chat_id=chat_id)
    notifier.send(body)


if __name__ == '__main__':
    main()

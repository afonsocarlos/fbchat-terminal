# -*- coding: utf-8 -*-

"""
    Terminal facebook messenger in python.

    obs: in case Windows command prompt exit with charmap codec error
    run the command chcp 65001 in it to fix the problem.
"""

from datetime import datetime

import fbchat
import sys


class Chat():

    def __init__(self, username, password):
        self.client = fbchat.Client(username, password)
        try:
            from colorama import Fore, Back, Style
            import colorama

            colorama.init()
            self.label = Fore.WHITE + Back.BLUE + Style.BRIGHT
            self.endlabel = Style.RESET_ALL
        except ImportError:
            self.label = ""
            self.endlabel = ""

    def choose_friend(self):
        friend = input("Who do you want to talk to: ")
        users = self.client.getUsers(friend)

        option = 0
        if len(users) > 1:
            print("Which of these friends?")
            for i, user in enumerate(users):
                print("%d. %s" % (i, user.name))

        try:
            option = int(input())
            self.friend = users[option].name
            self.userid = users[option].uid
        except ValueError as e:
            print("Option must be a number")
            raise e
        except IndexError as e:
            print("Invalid Index")
            raise e

    def chat(self):
        user_thread = self.client.getThreadInfo(self.userid, 0)

        while True:
            current = "you"
            for message in reversed(user_thread):

                if int(message.author.split(':')[1]) == self.userid:
                    if current == "you":
                        current = self.friend
                        print("%s %s: %s" % (self.label, current, self.endlabel))
                else:
                    if current == self.friend:
                        current = "you"
                        print("%s %s: %s" % (self.label, current, self.endlabel))

                try:
                    print("%s - %s" % (message.timestamp_datetime, message.body))
                except Exception:
                    # remember to set chcp 65001 on windows to make cmd utf8 compatible
                    print("%s - %s" % (message.timestamp_datetime, message.body.encode('cp860', errors='ignore')))

            send_message = input("type your message: ")

            if send_message:
                if send_message == "exit()":
                    sys.exit()
                elif send_message == "new_chat()":
                    break
                elif send_message == "help()":
                    self._show_help()
                else:
                    self.client.send(self.userid, send_message)

            user_thread = self.client.getThreadInfo(self.userid, 0)

    def _show_help(self):
        print("You can type these commands while talking to your friend:")
        print("new_chat() -> change friend to chat.")
        print("exit() -> exit this program.")
        print("help() -> show this help message.")
        input("Hit Enter to continue...")

def main():
    username = input("username: ")
    password = input("password: ")

    chat = Chat(username, password)

    del username
    del password

    print("Welcome to fbchat-terminal")
    chat._show_help()

    while True:
        chat.choose_friend()
        chat.chat()


if __name__ == '__main__':
    main()

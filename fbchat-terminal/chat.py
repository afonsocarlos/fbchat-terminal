# -*- coding: utf-8 -*-

"""
    Terminal facebook messenger in python.
    obs: in case Windows command prompt exit with charmap codec error
    run the command chcp 65001 in it to fix the problem.
"""

from datetime import datetime
from passlib.hash import pbkdf2_sha256

import fbchat
import getpass
import labels
import os, sys


class Chat():

    def __init__(self, username, password):
        self.client = fbchat.Client(username, password)
        self.client.password = pbkdf2_sha256.encrypt(self.client.password, rounds=1000, salt_size=16)
        self.chatting = True
       

    def lock_chat(self):
        ''' Lock chat.
            Hide messages and lock messenger until the correct
            password or exit() command is entered
        '''
        message = ''
        while not pbkdf2_sha256.verify(message, self.client.password):
            clear()
            message = getpass.getpass(">>")
            if message == "exit()":  # gives the option to exit
                sys.exit()
        # Completely unnecessary! (I think.. But maybe it prevents password to be hacked '-')
        message = None
        del message

    def choose_friend(self):
        '''Choose a friend to talk to according to the name user input.'''
        friend = input("Who do you want to talk to: ")
        users = self.client.getUsers(friend)

        option = 0
        if len(users) <= 0:
            print("No friends found.")
            print("Try again.")
            self.choose_friend()
        elif len(users) > 1:
            print("Which of these friends?")
            for i, user in enumerate(users):
                print("%d. %s" % (i, user.name))

        try:
            option = int(input())
            self.friend = users[option].name
            self.userid = users[option].uid
        except ValueError as e:
            print("Option must be a valid number.")
            print("Try again.")
            # recursion certainly is not the best solution here, but it was the easiest
            self.choose_friend()
        except IndexError as e:
            print("Invalid Index")
            raise e

    def chat(self):
        '''Chat with chosen friend.'''
        self.chatting = True
        
        while self.chatting:
            current = "you"
            friend_thread = self.client.getThreadInfo(self.userid, 0)

            for message in reversed(friend_thread):

                if int(message.author.split(':')[1]) == self.userid:
                    if current == "you":
                        current = self.friend
                        print("%s%s: %s" % (labels.START_LABEL, current, labels.END_LABEL))
                else:
                    if current == self.friend:
                        current = "you"
                        print("%s%s: %s" % (labels.START_LABEL, current, labels.END_LABEL))

                try:
                    print("%s - %s" % (message.timestamp_datetime, message.body))
                except Exception:
                    # remember to set chcp 65001 on windows to make cmd utf8 compatible
                    print("%s - %s" % (message.timestamp_datetime,
                                       message.body.encode('cp860', errors='ignore')))

            message = input("type your message: ")
            if message:
                if message == "exit()":
                    sys.exit()
                if message == "lock()":  # this will hide chat from eavesdroppers
                    self.lock_chat()
                elif message == "new_chat()": 
                    self.chatting = False
                elif message == "help()":
                    self._show_help()
                else:
                    self.client.send(self.userid, message)

    def _show_help(self):
        print("You can type these commands while talking to your friends:")
        print("new_chat() -> change friend to chat.")
        print("exit() -> exit this program.")
        print("help() -> show this help message.")
        input("Hit Enter to continue...")


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    # disguising application
    os.system('title Terminal')  # check if it works in Linux

    username = input("username: ")
    password = getpass.getpass("password: ")

    chat = Chat(username, password)

    username = password = None
    del username
    del password

    print(labels.START_TITLE + "********************************" + labels.END_TITLE)
    print(labels.START_TITLE + "*  Welcome to fbchat-terminal  *" + labels.END_TITLE)
    print(labels.START_TITLE + "********************************" + labels.END_TITLE)
    
    chat._show_help()

    while True:
        chat.choose_friend()
        chat.chat()


if __name__ == '__main__':
    main()
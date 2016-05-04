# -*- coding: utf-8 -*-

"""
	Terminal facebook messenger in python.

	obs: in case Windows command prompt exit with charmap codec error
	run the command chcp 65001 in it to fix the problem.
"""

import fbchat
import time  # new implementation - added with all comments replication below

def main():
	username = input("username: ")
	password = input("password: ")
	
	client = fbchat.Client(username, password)
	del username
	del password
	
	friend = input("Who do you want to talk to: ")
	userid = client.getUsers(friend)[0].uid
	user_thread = client.getThreadInfo(userid, 0)
	
	while True:
		current = "you"
		for message in reversed(user_thread):
			
			if int(message.author.split(':')[1]) == userid:
				if current == "you":
					current = friend
					print("%s:" % current)
			else:
				if current == friend:
					current = "you"
					print("%s:" % current)

			print(message.body.encode('cp860', errors='ignore'))

		#  remember to set chcp 65001 on windows to make cmd utf8 compatible
		send_message = input("type your message: ")
		
		if send_message:
			client.send(userid, send_message)

		user_thread = client.getThreadInfo(userid, 0)

if __name__ == '__main__':
	main()
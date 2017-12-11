import config
import time
import os
import praw

def reddit_login():
    reddit = praw.Reddit(
        client_id = config.CLIENT_ID,
        client_secret = config.CLIENT_SECRET,
        password = config.PASSWORD,
        user_agent = config.USER_AGENT,
        username = config.USERNAME)
    return reddit

def retrieve_usernames():
    if not os.path.isfile("usernames.txt"):
        usernames = []
    else:
        with open("usernames.txt", "r") as text_file:
            usernames = text_file.read()
            usernames = usernames.split("\n")
    return usernames

def retrieve_karma():
    if not os.path.isfile("karma.txt"):
        karma = []
    else:
        with open("karma.txt", "r") as text_file:
            karma = text_file.read()
            karma = karma.split("\n")
    return karma

def run_bot(reddit, usernames, karma):
    k = 0
    for comment in reddit.subreddit(config.SUBREDDIT_TARGET).comments(limit=100):
        user = comment.author
        if user.name not in usernames and user != None:
            score = user.link_karma + user.comment_karma
            usernames.append(user.name)
            karma.append(score)
            k += 1
    print(str(k) + " " "new entries have been added. " "There are " + str(len(usernames)) + " Total entries now.")

def sort_lists(usernames, karma):
    sorted_usernames = [x for _, x in sorted(zip(karma, usernames), reverse=True)]
    sorted_karma = sorted(karma, reverse = True)
    return sorted_usernames, sorted_karma

def list_to_text(usernames, karma):
    if len(usernames) == len(karma):
        with open("Usernames and Total Karma.txt","a") as text_file:
            for x in range (0,len(usernames)):
                text_file.write(str(usernames[x]) + "    " + str(karma[x]) + "\n")
    else:
        print("number of usernames in the list is not the same as the number of karma entries")

def remove_space(myList):
    while "" in myList:
        myListst.remove("")
    return myList


print("The script has started running.")
reddit = reddit_login()
print("Bot logged in as " + reddit.user.me().name)
usernames = retrieve_usernames()
karma = retrieve_karma()

while len(usernames) < config.MAXIMUM_NUMBER_OF_USERNAMES:
    run_bot(reddit, usernames, karma)
    time.sleep(1)

print("removing ''")
usernames = remove_space(usernames)
karma = remove_space(karma)
print("sorting two lists")
sorted_usernames, sorted_karma = sort_lists(usernames, karma)
print("writing into text file")
list_to_text(sorted_usernames, sorted_karma)
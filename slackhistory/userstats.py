''' Functions for collecting some statistics about users. 
'''
import argparse
from collections import Counter
import re

from slackhistory.historytools import *


def get_user_stats(history, users):
    ''' Add some additional statistics to the list of users (including number
    of posts in each channel, number of mentions of each other user, number
    of times mentioned by each other user, and so on.) 
    
    "history" should be the full history, not "posts only".
    '''
    user_stats = {}
    for user in users:
        user_stats[user["id"]] = {
            "user_info":user,
            "id":user["id"],
            "name":user["name"],
            "real_name":user["profile"]["real_name"],
            "posts_per_channel": Counter(),
            "mentions_per_user": Counter(),  # Mentions of other users.
            "mentioned_per_user": Counter(), # Times mentioned by others.
            "joined": None,
            "first_post_time": None,
            "last_post_time": None,
            "questions": Counter()  # Number of questions asked
        }

    # Also handle slackbot
    user_stats["USLACKBOT"] = {
        "id":"USLACKBOT",
        "name":"slackbot",
        "real_name":"Slack Bot",
        "user_info": None,
        "posts_per_channel": Counter(),
        "mentions_per_user": Counter(), 
        "mentioned_per_user": Counter(),
        "joined": None,
        "first_post_time": None,
        "last_post_time": None,
        "questions": Counter()
    }
    posts = flatten_posts(history)
    for post in posts:
        if post["channel"] == "general":
            # To determine join date, we assume that every member will have
            # a "joined" message in the general channel.
            pass
        # Otherwise, we ignore all posts that are not text posts by humans.
        elif is_text_post(post):
            user = post["user"]
            user_stats[user]["posts_per_channel"][post["channel"]] += 1
            user_stats[user]["questions"] += count_questions(post)
            for mu in mentioned_users(post):
                user_stats[user]["mentions_per_user"][mu] += 1
                user_stats[mu]["mentioned_per_user"][user] += 1
            # Check post times
            first_post = user_stats[user]["first_post_time"]
            last_post = user_stats[user]["first_post_time"]
            if first_post == None or post["ts"] < first_post:
                user_stats[user]["first_post_time"] = post["ts"]
            if last_post == None or post["ts"] > last_post:
                user_stats[user]["last_post_time"] = post["ts"]
    return user_stats

def count_questions(post):
    ''' Count the number of questions (well, question marks) in a post. '''
    return post["text"].count("?")


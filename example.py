''' An example script using functions from slack_history_loader to collect some
data about members of a slack channel.

We count number of questions asked and total number of posts by each user,
as well as the total number of times each poster has been @'ed by others,
and the total number of times that each poster has been @'ed in a post
containing a question.
'''
import argparse
from collections import Counter
import re

from slack_history_loader import load_history, flatten_posts, remove_channels


def count_questions(post):
    ''' Count the number of questions (well, question marks) in a post. '''
    return post["text"].count("?")

def mentioned_users(post):
    ''' Get a list of all user ids that were @'ed in a post. '''
    return re.findall("<@([A-Z0-9]*?)>",post["text"])

# Start the main script
if __name__=="__main__":
    # usage: python example.py ./path/to/slack/data/ > output.csv

    parser = argparse.ArgumentParser(description="This script measures some "
        + "aspects of users' behaviour in a Slack workspace, and prints the "
        + "data to stdout in csv format.")
    parser.add_argument("datadir", help="The directory containing "
        + "your exported (uncompressed) Slack data.")
    args = parser.parse_args()

    # Load history, excluding the random channel
    history, users = load_history(args.datadir, text_only=False)
    history = remove_channels(history,["random"])
    posts = flatten_posts(history)
    id2name = {user["id"]:user["profile"]["real_name"] for user in users}

    # Count stuff.
    # Note: I will index users by id.
    questions_asked = Counter()
    total_posts = Counter()
    mentions = Counter()
    requests = Counter() # Mentions in posts containing a question
    for post in posts:
        questions_asked[post["user"]] += count_questions(post)
        total_posts[post["user"]] += 1
        for uid in mentioned_users(post):
            mentions[uid] += 1
            if count_questions(post) >= 1:
                requests[uid] += 1

    # Print to stdout in CSV format
    print("user, questions asked, posts, mentions, question mentions")
    for uid, name in id2name.items():
        try:
            # Python 3 (maybe also 2 if the data is behaving nicely?):
            print("%s, %d, %d, %d, %d" % (name, 
                questions_asked[uid], total_posts[uid], 
                mentions[uid], requests[uid]))
        except:
            # Python 2:
            print("%s, %d, %d, %d, %d" % (name.encode("utf-8"), 
                questions_asked[uid], total_posts[uid], 
                mentions[uid], requests[uid]))


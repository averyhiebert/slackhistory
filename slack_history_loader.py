''' 
This script contsins some functions for loading an exported slack history 
and doing stuff with it.  It won't work for very, very large histories 
(i.e. too big to fit in RAM), but this shouldn't be a problem for most 
Slack teams.

You shouldn't need to install any other dependencies to use this.  It should
work with Python 2 or 3.


MIT License

Copyright 2018 Avery Hiebert

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''
import argparse
import os 
import json
import re
import copy

def load_history(dirname,channel_filter=None,text_only=True,posts_only=True):
    ''' 
    With dirname being the directory containing a slack backup,
    load the contents into a dict of the form
    {"channel1":[post1, post2, post3, and so on],"channel2":[...]...}.
        
    If channel_filter is given, only channels in the list will be included.
    If text_only is True, only the text of each post, rather than all the
        metadata, is stored.
    If posts_only is True, then only real human posts (not bot posts,
        file shares, channel join notifications etc.) are included.
    '''
    # Load the list of user ids/names
    #  (Needed for replacing username mentions with user names)
    with open("%s/users.json" % dirname,"r") as f:
        users = json.load(f)

    # Get the list of subdirectories and filter out unwanted channels.
    #  (assumes anything not containing a "." is a directory)
    channels = [d for d in os.listdir(dirname) if "." not in d]
    if channel_filter:
        channels = [d for d in channels if d in channel_filter]

    # Get the files for each channel
    history = {channel:[] for channel in channels}
    for channel in channels:
        # (names are dates in year-month-day format, 
        #  so sorting lexicographically also sorts chronologically)
        filenames = sorted(os.listdir(dirname+"/"+channel))
        # Filter out hidden files, just in case.
        filenames = [f for f in filenames if f[0] != "."]
        for fname in filenames:
            with open(dirname + "/" + channel + "/" + fname,"r") as f:
                data = json.load(f)
            for item in data:
                if posts_only:
                    if item["type"] != "message": continue
                    if "subtype" in item: continue
                    if "bot_id" in item: continue
                if text_only:
                    history[channel].append(item["text"])
                else:
                    history[channel].append(item)
    return history, users

def remove_channels(history,channels):
    ''' Remove a given set of channels from the history. '''
    return {channel:data for channel, data in history.items() 
        if channel not in channels}

def sub_usernames(post, id2user):
    ''' Find any user name mentions in the post, and replace with the
        @username string.  
       
        If "post" is a string, we return the new string.
        If "post" is a dict, we return the new dict with modified text,
            and also replace the "user" field with a user name.'''
    # Have to handle Slackbot as well
    id2user["USLACKBOT"] = "slackbot"

    # Sorry for this slight awkwardness - trying to support python 2 and 3.
    string_types = [str]
    try:
        string_types = [unicode, str]
    except:
        # We must be using Python 3, where unicode type isn't a thing anymore.
        pass

    if type(post) in string_types:
        # Substitute user names in string
        def user_id_helper(match):
            return "@" + id2user[match.group(0)[2:-1]]
        new_str = re.sub(r"<@[A-Z0-9]*?>", user_id_helper, post)
        new_str = re.sub(r"<!channel>", "@channel", new_str)
        new_str = re.sub(r"<!everyone>", "@everyone", new_str)
        return new_str
    elif type(post["text"]) in string_types:
        # Recursively call on the string portion of the post.
        new_post = copy.deepcopy(post)
        new_post["text"] = sub_usernames(post["text"], id2user)
        new_post["user"] = id2user[post["user"]]
        return new_post
    # Should probably include some sort of error handling here...

def tidy_history(history, users):
    ''' Given a history dict, make it a bit nicer to use.
    (Right now, this will just fix user mentions in every post.)

    This does not modify the original object.'''
    id2user = {user["id"]:user["name"] for user in users}
    new_history = {channel:[] for channel in history.keys()}
    for channel, post_list in history.items():
        fixed_list = [sub_usernames(post, id2user) for post in post_list]
        new_history[channel] = fixed_list
    return new_history

def flatten_posts(history):
    ''' Flatten all posts from all channels into a single list '''
    posts = []
    for post_list in history.values():
        posts = posts + post_list
    return posts

def remove_urls(post_list):
    ''' Make a list of posts marginally more safe to host on 3rd-party
    services (for e.g. a slack bot?) by removing any posts containing urls,
    in case you're worried about Google Docs links in your Slack history
    or something like that.'''
    # This is a rough heuristic - especially not great if you
    #  discuss web development a lot on Slack!
    return [post for post in post_list if "http" not in post]

def add_period(post):
    ''' Not all posts on slack end in punctuation.  But maybe you want
    them to. '''
    if len(post.strip()) < 1:
        return post
    if post.strip()[-1] not in [".","?","!"]:
        return post.strip() + "."
    return post
        

if __name__=="__main__":
    # A main program for demonstration purposes.
    #  Run this to create a text file containing a record of your team's
    #  history that can easily be used with the Markovify library
    #  to generate sentences resembling your team's Slack discussions!
    parser = argparse.ArgumentParser(
        description="Demo script for working with Slack history - creates "
        + "a text file containing the concatenation of all posts from "
        + "your Slack team's history.")

    parser.add_argument("--slack-data-dir", default="./data",
        help="The directory containing your extracted slack data.")
    parser.add_argument("--output-file", default="./slack_history.txt",
        help="The file to write your results to.")
    args = parser.parse_args()

    # Load and (partially) sanitize the history.
    history, users = load_history(args.slack_data_dir,text_only=True)
    nice_history = tidy_history(history, users)
    safer_posts = remove_urls(flatten_posts(nice_history))

    # Create a document that works well with Markovify.
    finalized_posts = [add_period(p) for p in safer_posts]
    document = "\n".join(finalized_posts)

    # Save the document
    with open(args.output_file,"w") as f:
        try:
            # Python 3
            f.write(document)
        except:
            # Python 2?
            f.write(document.encode("utf-8"))

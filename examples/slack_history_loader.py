''' 
Example script which creates a single text file containing a record
of your team's history, which can easily be used with the Markovify library
to generate sentences resembling your team's Slack discussions!
'''

import argparse
from slackhistory import historytools as ht

if __name__=="__main__":
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
    history, users = ht.load_history(args.slack_data_dir,text_only=True)
    nice_history = ht.tidy_history(history, users)
    safer_posts = ht.remove_urls(ht.flatten_posts(nice_history))

    # Create a document that works well with Markovify.
    finalized_posts = [ht.add_period(p) for p in safer_posts]
    document = "\n".join(finalized_posts)

    # Save the document
    with open(args.output_file,"w") as f:
        try:
            # Python 3
            f.write(document)
        except:
            # Python 2?
            f.write(document.encode("utf-8"))

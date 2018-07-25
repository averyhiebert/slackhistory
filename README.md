# Slack History Loader

The script `slack_history_loader.py` defines some functions for loading the 
many directories of JSON files obtained when exporting history from a Slack
workspace.  Instructions for exporting your workspace's history can
be found [here](https://get.slack.help/hc/en-us/articles/201658943-Export-your-workspace-data) (at the time of writing, at least).
If you're looking for a more fully-featured tool for viewing your Slack 
history, try 
[slack-export-viewer](https://github.com/hfaran/slack-export-viewer) instead.

You'll need to extract the downloaded zip before using this library to load it.

## Usage examples.

The "main" code at the bottom of `slack_history.py` demonstrates how to
use these functions to load the exported history data and create a text file
containing every text post.  You could use this
along with [Markovify](https://github.com/jsvine/markovify) to create a
bot that writes posts mimicking your team's posting behaviour.

In addition, `example.py` calculates some statistics about a team's Slack
usage.

## License

Released under the MIT license, which I placed in a comment at the top
of `slack_history_loader.py` in lieu of including a separate LICENSE.txt file.

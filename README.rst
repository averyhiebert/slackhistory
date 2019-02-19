Slack History
=============

This library contains some utilities for loading the 
many directories of JSON files obtained when exporting history from a Slack
workspace.  Instructions for exporting your workspace's history can
be found `here <https://get.slack.help/hc/en-us/articles/201658943-Export-your-workspace-data>`_ (at the time of writing, at least).
If you're looking for a user-friendly tool for viewing your Slack history, try 
`slack-export-viewer <https://github.com/hfaran/slack-export-viewer>`_ instead.

You'll need to extract the downloaded zip before using this library to load it.

Usage examples.
---------------

The script ``examples/create_summary.py`` demonstrates how to
use these functions to load the exported history data and create a text file
from the contents of every text post.  You could use this
along with `Markovify <https://github.com/jsvine/markovify>`_ to create a
bot that writes posts mimicking your team's posting behaviour.

In addition, ``examples/example.py`` collects some data about a team's Slack usage.

License
-------

Released under the MIT license, as described in `LICENCE.txt`

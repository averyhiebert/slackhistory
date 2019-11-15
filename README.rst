Slack History
=============

This library contains some utilities for loading the 
many directories of JSON files obtained when exporting history from a Slack
workspace.  Instructions for exporting your workspace's history can
be found `here <https://get.slack.help/hc/en-us/articles/201658943-Export-your-workspace-data>`_ (at the time of writing, at least).
If you're looking for a user-friendly tool for viewing your Slack history, try 
`slack-export-viewer <https://github.com/hfaran/slack-export-viewer>`_ instead.

You'll need to extract the downloaded history zip before using this 
library to load it.

Sorry for the lack of documentation; this was only intended for my own personal
use, but I'm making it public anyways because, all things considered, there's
really no reason not to.

Usage examples.
---------------

The script ``examples/create_summary.py`` demonstrates how to
use these functions to load the exported history data and create a text file
containing the contents of every text post, separated by newlines.  
You could use this along with 
`Markovify <https://github.com/jsvine/markovify>`_ to create a
bot that writes posts mimicking your team's posting behaviour.
(This was the original motivation for the project).

In addition, ``examples/example.py`` collects some data about a team's 
Slack usage.

License
-------

Released under the MIT license, as described in `LICENCE.txt`

#Reddit Poll Bot

##Description
A poll creation and management bot for Reddit.

Using the Reddit API for communication, this class can create, destroy, and
manage polls for users on the popular social news site, reddit.com.

##Author
Created by [Evan Sneath](http://github.com/evansneath)

##License
This software licensed under the [Open Software License v3.0](http://www.opensource.org/licenses/OSL-3.0).

##Dependencies
In order to run, this software requires the following dependencies

* [Python 2.7](http://python.org/)
* [Reddit API Wrapper for Python 1.3.8](https://github.com/mellort/reddit_api)

The class might work with other versions of the dependencies, but they have not been tested.

##Usage
The Reddit Poll Bot class is easy to use and modify for specific needs. Here are some specific use case examples.

###Creating a new bot and submission
```python
import reddit_poll_bot

bot = reddit_poll_bot.RedditPollBot("My poll bot's user-agent id")
bot.login('bot_username', 'bot_password')

subreddit = 'aww'
title = 'Vote for the cutest animal!'
description = 'Which do you like best?'
candidates = ['dog', 'cat', 'lizard']
bot.create_poll(subreddit, title, description, candidates)
```
Once created, Reddit users may comment on the submission and place their vote by italicizing their choice of candidate anywhere in their comment. This is done by surrounding their choice with asterisks.

Example:
```
My favorite is the *lizard*!
```

###Deleting a poll
```python
bot.delete_poll('Vote for the cutest animal!')
```

###Ending a poll and posting the results
Reddit Vote Bot will automatically tally all of the votes and edit the submission for everyone to see.
```python
bot.post_votes('Vote for the cutest animal!', show_winner=True)
```
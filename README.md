#Reddit Poll Bot

##Description
A poll creation and management bot for Reddit.

Using the Reddit API for communication, this class can create, destroy, and
manage polls for users on the popular social news site, [Reddit](http://reddit.com).

##Author
Created by [Evan Sneath](http://github.com/evansneath).

##License
This software licensed under the [Open Software License v3.0](http://www.opensource.org/licenses/OSL-3.0).

##Dependencies
In order to run, this software requires the following dependencies:

* [Python 2.7](http://python.org/)
* [Reddit API Python Wrapper 1.3.8](https://github.com/mellort/reddit_api)

The class might work with other versions of the dependencies, but they have not been tested.

##Usage
The Reddit Poll Bot class is easy to use and modify for specific needs. Documentation is kept up-to-date
in the source code. Here are some simple use case examples.

###Creating a new bot and submission
This creates a new poll and automatically generates body text for the submission using the title, description, and candidates list.
```python
import reddit_poll_bot

# connect to reddit api
bot = reddit_poll_bot.RedditPollBot("My poll bot's user-agent id")
bot.login('bot_username', 'bot_password')

# create the poll
subreddit = 'aww'
title = 'Vote for the cutest animal!'
description = 'Which do you like best?'
candidates = ['dog', 'cat', 'lizard']
bot.create_poll(subreddit, title, description, candidates)
```
Once created, Reddit users may comment on the submission and place their vote by italicizing their 
choice of candidate anywhere in their comment. This is done by surrounding their choice with 
asterisks. For example:
```
My favorite animals are *lizard*s!
```

###Seeing intermittent poll results
The ```peek_vote()``` method of the Reddit Vote Bot can be used to unintrusively see results at any 
time in the polling process. Below is an example where all valid choices and their current voting 
results are printed.
```python
# define valid voting choices
candidates = ['dog', 'cat', 'lizard']
title = 'Vote for the cutest animal!'

# print each poll choice and its vote count
for candidate, count in bot.peek_votes(title, candidates).items():
    print 'choice: ' + candidate + ' votes: ' + str(count)
```

###Ending a poll and posting the results
Reddit Vote Bot will automatically tally all of the votes and edit the submission for everyone to see. 
Entering the candidates list restricts accepted entries to those candidates.
```python
# count votes and post the results to the poll
title = 'Vote for the cutest animal!'
candidates = ['dog', 'cat', 'lizard']
bot.post_votes(title, candidates, show_winner=True)
```

###Deleting a poll
This removes the poll submission from Reddit.
```python
# delete this poll forever
bot.delete_poll('Vote for the cutest animal!')
```
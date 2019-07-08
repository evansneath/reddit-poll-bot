import re
from collections import defaultdict

import praw


class RedditPollBot(object):
    """A poll creation and management bot for Reddit

    Using the Reddit API for communication, this class can create, destroy, and
    manage polls for users on the popular social news site, reddit.com.

    Attributes:
        reddit_api: Holds the Praw API object for use in class methods
        user: Holds the bot's API user object for finding submissions
    """
    reddit_api = None
    user = None

    def __init__(self, username, password, user_agent, client_id, client_secret):
        """Initialize the RedditPollBot class

        Begins the Reddit API with the inputted user agent id.

        Args:
            user_agent: The required bot id
        """
        # connect bot to reddit
        self.reddit_api = praw.Reddit(client_id=client_id,
                                 client_secret=client_secret,
                                 user_agent=user_agent,
                                 username=username,
                                 password=password)
        self.user = self.reddit_api.user.me()

    def create_poll(self, subreddit, title, description, candidates):
        """Creates a bot submission and the platform for a poll

        By creating a new submission under the bot's account, this allows for
        future editting and data collecting by the RedditPollBot.

        Args:
            subreddit: The subreddit in which to submit the poll
            title: The title of the poll (this will be the submission title)
            description: A poll description to be added to the poll text
            candidates: A list of strings naming candidates for the poll

        Returns:
            Newly created Reddit API submission object
        """
        instructions = ('To vote for an entry, place the entry name '
                        'surrounded by asterisks somewhere in your comment.')
        example = r"Example: I'm voting for \*bacon\*!"

        # add description to body text
        text = description + '\r\n\r\n'

        # add each candidate into body text
        for candidate in candidates:
            text += ' * ' + candidate + '\r\n'

        # add instructions and example vote to body text
        text += '\r\n' + instructions + '\r\n\r\n' + example

        return self.reddit_api.subreddit(subreddit).submit(title, text)

    def delete_poll(self, title):
        """Deletes a poll

        Given a poll title created by the logged in RedditPollBot, this will
        delete a poll submission.

        Args:
            title: The exact title of the poll to delete

        Returns:
            True on success, False on failure
        """
        # delete submission created by the bot with the specified title
        poll = self._find_poll(title)

        poll.delete()

        return True

    def post_votes(self, title, candidates=None, show_winner=True):
        """Posts submission votes

        Updates the given poll with a full count of all votes casted and shows
        the winner if desired.

        Args:
            title: The exact title of the poll to count and post votes
            candidates: A list of candidates to select from votes. If this is
                none, any italicized item will be accepted.
            show_winner: A boolean indicating if the winner should be displayed

        Returns:
            True on success, False on failure
        """
        # update the submission text with the newest amount of votes
        poll = self._find_poll(title)
        votes = self.peek_votes(title, candidates)
        print(votes)

        if not votes:
            return False

        # compile text for updated poll
        text = poll.selftext + '\r\n\r\n'
        text += 'THE VOTES ARE IN // POLLING IS CLOSED\r\n'
        text += '-------------------------------------\r\n\r\n'
        text += 'RESULTS:                             \r\n\r\n'

        # display vote numbers
        for candidate, count in votes.items():
            text += ' * ' + candidate + ' : ' + str(count) + '\r\n'

        # display a winner if desired
        if show_winner:
            text += '\r\nWINNER: ' + max(votes) + '\r\n'

        # edit the pol to include the results
        editted = False
        if poll.edit(text) is not None:
            editted = True

        return editted

    def peek_votes(self, title, candidates=None):
        """Peek at the current votes

        Given a poll object, this method will output a list of tuples of the
        candidates and their current vote counts.

        Args:
            title: The exact title of the poll to see current votes
            candidates: A list of candidates to select from votes. If this is
                None, any italicized item will be accepted.

        Returns:
            Dict with candidate name as key and number of votes as value
        """
        votes = defaultdict(int)

        # find a poll of the given title
        poll = self._find_poll(title)

        for comment in poll.comments:
            # get the first value surrounded by asterisks
            vote = re.search(r'\*([a-zA-Z0-9_ ]*)\*', comment.body)

            if vote is not None:
                # return lowercase version of the key without asterisks
                vote = vote.group(1).lower()

                # determine if the italicized value found is valid for the poll
                if candidates is None or vote in candidates:
                    votes[vote] += 1

        return votes

    def _find_poll(self, title):
        """Find a poll of a given title

        Given a title, a search will be made for a poll submission of that
        exact title.

        Args:
            title: The exact title of the poll to find

        Returns:
            Reddit API submission object if found, None otherwise
        """
        # find a submission with a given title
        found = None

        for poll in self.user.submissions.new(limit=None):
            if poll.title == title:
                return poll

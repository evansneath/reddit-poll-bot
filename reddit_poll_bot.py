import reddit
import re

class RedditPollBot(object):
    """A poll creation and management bot for Reddit
    
    Using the Reddit API for communication, this class can create, destroy, and
    manage polls for users on the popular social news site, reddit.com.
    
    Note that it is customary for Reddit bots to have a 2 second delay between
    API requests. This is noted on the Reddit API rules:
    https://github.com/reddit/reddit/wiki/api
    
    Requires the Reddit API for Python:
    https://github.com/mellort/reddit_api
    
    Attributes:
        username: The Reddit username of the bot
        password: The Reddit password of the bot
        user_agent: The required bot id. see the API rules for more details
        user: Holds the bot's user object once logged in
    """
    username = ''
    password = ''
    user_agent = ''
    reddit_api = None
    user = None

    def __init__(self, user_agent):
        """Initialize the RedditPollBot class
        
        Begins the Reddit API with the inputted user agent id.
        
        Args:
            user_agent: The required bot id
        """
        super(RedditPollBot, self).__init__()
        
        # connect bot to reddit
        self.reddit_api = reddit.Reddit(user_agent=user_agent)

    def login(self, username, password):
        """Logs the bot into Reddit
        
        Logging the bot into Reddit is required for most methods in this class
        and is highly recommended after object initialization.
        
        Args:
            username: The Reddit username of the bot
            password: The Reddit password of the bot
        """
        self.username = username
        self.password = password
        
        # login bot to reddit
        self.reddit_api.login(username, password)
        self.user = self.reddit_api.get_redditor(self.username)
    
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
        instructions = 'To vote for an entry, place the entry name surrounded by asterisks somewhere in your comment.'
        example = 'Example: \*your choice\*'
        
        # add description to body text
        text = description + '\r\n\r\n'
        
        # add each candidate into body text 
        for candidate in candidates:
            text = text + ' * ' + candidate + '\r\n'
        
        # add instructions and example vote to body text
        text = text + '\r\n' + instructions + '\r\n\r\n' + example
        
        return self.reddit_api.submit(subreddit, title, text=text)
    
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
        deleted = False
        poll = self.find_poll(title)
        
        if poll is not None:
            poll.delete()
            deleted = True
        
        return deleted
    
    def post_votes(self, title, show_winner=True):
        """Posts submission votes
        
        Updates the given poll with a full count of all votes casted and shows
        the winner if desired.
        
        Args:
            title: The exact title of the poll to count and post votes
            show_winner: A boolean indicating if the winner should be displayed
        
        Returns:
            True on success, False on failure
        """
        # update the submission text with the newest amount of votes
        poll = self.find_poll(title)
        votes = self.peek_votes(poll)
        winner = (None, 0)
        
        # compile text for updated poll
        text =  'THE VOTES ARE IN // POLLING IS CLOSED\r\n'
        text += '-------------------------------------\r\n'
        text += 'RESULTS:                             \r\n\r\n'
        
        # display vote numbers
        for vote in votes:
            text += ' * ' + str(vote[0]) + ' : ' + str(vote[1]) + '\r\n\r\n'
            if int(vote[1]) > winner[1]:
                winner = vote
        
        # display a winner
        if show_winner:
            text += '\r\nWINNER: ' + str(winner[0]) + '\r\n'
        
        if poll.edit(text) is not None:
            return True
        else:
            return False
    
    def peek_votes(self, poll):
        """Peek at the current votes
        
        Given a poll object, this method will output a list of tuples of the
        candidates and their current vote counts.
        
        Args:
            poll: A Reddit API submission object of which to count current votes
        
        Returns:
            List of tuples with the candidate name and current number of votes
            
            example:
                ('candidate1':3)
                ('candidate2':5)
        """
        votes = dict()
        
        for comment in poll.comments:
            # get the first value surrounded by strings
            vote = re.search('\*\S*\*', str(comment)).group()
            # return lowercase version of the key w/o spaces and asterisks
            vote = vote[1:len(vote)-1].strip().lower()
            
            # create a new key if it does not exist
            if vote not in votes:
                votes[vote] = 0
            
            # add a vote for the key
            votes[vote] += 1
        
        return votes.items()
    
    def get_polls(self):
        """Gets all bot posts
        
        Returns all submission by the logged in bot in enumerated form.
        
        Returns:
            Enumerated list of Reddit API submission objects.
        """
        return enumerate(self.user.get_submitted())
    
    def find_poll(self, title):
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
        
        for poll in self.get_polls():
            if poll[1].title == title:
                found = poll[1]
        
        return found
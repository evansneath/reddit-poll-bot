"""A setuptools based setup module.

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# io.open is needed for projects that support Python 2.7
# It ensures open() defaults to text mode with universal newlines,
# and accepts an argument to specify the text encoding
# Python 3 only projects can skip this import
from io import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='reddit_poll_bot',  # Required
    version='2.0.0',  # Required

    description='A poll bot for reddit',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)

    url='https://github.com/evansneath/reddit-poll-bot.git',  # Optional

    author='Evan Sneath',  # Optional
    # author_email='pypa-dev@googlegroups.com',  # Optional

    keywords='reddit praw poll bot',  # Optional
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required

    install_requires=['praw'],  # Optional


    entry_points={  # Optional
        'console_scripts': [
            'create_poll=reddit_poll_bot.entry_point:create_post',
            'update_post=reddit_poll_bot.entry_point:update_post',
            'delete_post=reddit_poll_bot.entry_point:delete_post',
        ],
    },
)

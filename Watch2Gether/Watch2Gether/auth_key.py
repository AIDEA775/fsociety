# -*- coding: utf-8 -*-
import os

APP_DIR = os.path.dirname(os.path.realpath(__file__))
DATABASE = 'sqlite:///{}'.format(os.path.join(APP_DIR, 'user.db'))
DEBUG = True
SECRET_KEY = 'development'


GOOGLE_ID = '705222363656-5ng8t00km43m9autga4sdc4jrn5sjm0q.apps.googleusercontent.com'
GOOGLE_SECRET = 'YktK-5yt8HRlmwUe0acfBXDz'

FACEBOOK_ID = '1798770117036103'
FACEBOOK_SECRET = '8292bc09a6835e8d328cfcfbbf5706b8'

TWITTER_ID = '6rNAfPUpjGgJZkkWswOFWM2vR'
TWITTER_SECRET = '8jAgdx8NArfD0w63Y7cehP880PEyxhbmbS1lpWK2vcgCkoYDYp'
    

import os
import json


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '1234ABCDabcd'
    UPLOAD_FOLDER = os.path.join(os.environ.get('UPLOAD_FOLDER')) or 'files'
    USERS = json.loads(os.environ.get("FLASK_USERS")) or \
            {'id': '1', \
             'name': 'user', \
             'password': 'user_test', \
             'active': 'True'}
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'py'])

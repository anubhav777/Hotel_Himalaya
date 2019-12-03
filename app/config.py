import os


class Parent(object):

    SQLALCHEMY_DATABASE_URI = os.environ.get('HIMALAYA_DB')
    SQLALCHEMY_TRACK_MODIFICATION = False
    ALLOWED_IMAGE_EXTENSION = ['JPG', 'JPEG', 'PNG']


class Production(Parent):
    pass


class Development(Parent):
    DEBUG = True

from google.appengine.ext import db

class Image(db.Model):
    blob_key = db.StringProperty()
    content_type = db.StringProperty()
    date = db.DateTimeProperty()

class Post(db.Model):
    username = db.StringProperty()
    url = db.StringProperty()
    date = db.DateTimeProperty()

class App(db.Model):
    name = db.StringProperty()
    secret = db.StringProperty()
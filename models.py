from google.appengine.ext import db

class Image(db.Model):
    data = db.BlobProperty()
    content_type = db.StringProperty()
    date = db.DateTimeProperty()

class Post(db.Model):
    username = db.StringProperty()
    url = db.StringProperty()
    date = db.DateTimeProperty()

class Auth(db.Model):
    app_name = db.StringProperty()
    secret = db.StringProperty()
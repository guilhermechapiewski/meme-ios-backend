from google.appengine.ext import db

class Image(db.Model):
    data = db.BlobProperty(default=None)
    content_type = db.StringProperty()
    date = db.DateTimeProperty(auto_now_add=True)
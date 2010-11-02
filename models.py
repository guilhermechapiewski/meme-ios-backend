from google.appengine.ext import db

class Image(db.Model):
    data = db.BlobProperty()
    content_type = db.StringProperty()
    date = db.DateTimeProperty()
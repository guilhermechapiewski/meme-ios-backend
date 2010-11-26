from google.appengine.ext import blobstore, webapp

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.redirect('http://memeapp.net')
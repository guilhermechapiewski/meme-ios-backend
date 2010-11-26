#!/usr/bin/env python
import wsgiref.handlers
from google.appengine.ext import blobstore, webapp

from handlers.admin import AdminHandler
from handlers.highlight import HighlightHandler, HighlightUpdateHandler
from handlers.image import ImageHandler, ImageUploadHandler, ImageUploadUrlHandler, ImageExpirationHandler
from handlers.main import MainHandler
from handlers.postlater import PostLaterHandler, PostLaterAddHandler, PostLaterDeleteHandler

def main():
    blobstore.MAX_BLOB_FETCH_SIZE = 7168 * 1024 #7MB
    
    application = webapp.WSGIApplication([
                ('/', MainHandler), 
                ('/admin', AdminHandler), 
                ('/highlight/update', HighlightUpdateHandler), 
                ('/highlight/(.+)', HighlightHandler), 
                ('/img/expiration', ImageExpirationHandler), 
                ('/img/upload/url', ImageUploadUrlHandler), 
                ('/img/upload', ImageUploadHandler), 
                ('/img/(.+)', ImageHandler), 
                ('/postlater/delete', PostLaterDeleteHandler), 
                ('/postlater/add', PostLaterAddHandler), 
                ('/postlater/(.+)', PostLaterHandler), 
            ], 
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()

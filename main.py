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
                ('/v1/highlight/update', HighlightUpdateHandler), 
                ('/v1/highlight/(.+)', HighlightHandler), 
                ('/v1/img/expiration', ImageExpirationHandler), 
                ('/v1/img/upload/url', ImageUploadUrlHandler), 
                ('/v1/img/upload', ImageUploadHandler), 
                ('/v1/img/(.+)', ImageHandler), 
                ('/v1/postlater/delete', PostLaterDeleteHandler), 
                ('/v1/postlater/add', PostLaterAddHandler), 
                ('/v1/postlater/(.+)', PostLaterHandler), 
            ], 
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()

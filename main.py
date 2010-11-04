#!/usr/bin/env python
import wsgiref.handlers
from google.appengine.ext import blobstore, webapp

from handlers.main import MainHandler
from handlers.image import ImageHandler, ImageUploadHandler, ImageExpirationHandler
from handlers.postlater import PostLaterHandler, PostLaterAddHandler, PostLaterDeleteHandler

def main():
    blobstore.MAX_BLOB_FETCH_SIZE = 7168 * 1024 #7MB
    
    application = webapp.WSGIApplication([
                ('/', MainHandler),
                ('/img/expiration', ImageExpirationHandler),
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

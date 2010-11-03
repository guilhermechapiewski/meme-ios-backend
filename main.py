#!/usr/bin/env python
import wsgiref.handlers
from google.appengine.ext import webapp

from handlers.main import MainHandler
from handlers.image import ImageHandler, ImageUploadHandler, ImageExpirationHandler
from handlers.postlater import PostLaterHandler, PostLaterAddHandler

def main():
    application = webapp.WSGIApplication([
                ('/', MainHandler),
                ('/img/expiration', ImageExpirationHandler),
                ('/img/upload', ImageUploadHandler),
                ('/img/(.+)', ImageHandler),
                ('/postlater/add', PostLaterAddHandler),
                ('/postlater/(.+)', PostLaterHandler),
            ], 
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()

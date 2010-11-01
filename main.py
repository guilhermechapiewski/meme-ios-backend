#!/usr/bin/env python
import wsgiref.handlers
from google.appengine.ext import db, webapp

from models import Image

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
        <html>
            <head>
                <title>Yahoo! Meme iOS Backend application</title>
            </head>
            <body>
                <form action="/img/upload" method="POST" enctype="multipart/form-data">
                    Upload File: <input type="file" name="file"><br>
                    Content-type: <select name="content_type"><option>image/gif</option><option>image/jpeg</option><option>image/png</option></select><br>
                    <input type="submit" name="submit" value="Submit">
                </form>
            </body>
        </html>
        ''')

class ImgHandler(webapp.RequestHandler):
    def get(self, img_key):
        image = None
        try:
            image = db.get(img_key)
        except:
            self.error(404)
            self.response.out.write('Image not found.')
        
        if image:
            self.response.headers['Content-Type'] = str(image.content_type)
            self.response.out.write(image.data)

class ImgUploadHandler(webapp.RequestHandler):
    def post(self):
        img_data = self.request.POST.get('file').file.read()
        content_type = self.request.POST.get('content_type')
        
        image = Image(data=img_data, content_type=content_type)
        image.put()
        
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write({ 
            'id': str(image.key()), 
            'url': 'http://%s/img/%s' % (self.request.headers['Host'], image.key()),
        })

def main():
    application = webapp.WSGIApplication([
                ('/', MainHandler),
                ('/img/upload', ImgUploadHandler),
                ('/img/(.+)', ImgHandler),
            ], 
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()

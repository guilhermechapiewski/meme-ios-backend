#!/usr/bin/env python
import wsgiref.handlers
from google.appengine.api import images
from google.appengine.ext import db, webapp
from google.appengine.ext.webapp.util import run_wsgi_app

class Image(db.Model):
    data = db.BlobProperty(default=None)

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
                    <input type="submit" name="submit" value="Submit">
                </form>
            </body>
        </html>
        ''')
        

class ImgHandler(webapp.RequestHandler):
    def get(self, img_key):
        image = db.get(img_key)
        self.response.headers['Content-Type'] = 'image/png'
        self.response.out.write(image.data)

class ImgUploadHandler(webapp.RequestHandler):
    def post(self):
        img_data = self.request.POST.get('file').file.read()

        try:
          img = images.Image(img_data)
          img.im_feeling_lucky()
          #png_data = img.execute_transforms(images.PNG)

          stored_image = Image(data=img_data)
          stored_image.put()

          self.redirect('/img/%s' % stored_image.key())
        except images.BadImageError:
          self.error(400)
          self.response.out.write(
              'Sorry, we had a problem processing the image provided.')
        except images.NotImageError:
          self.error(400)
          self.response.out.write(
              'Sorry, we don\'t recognize that image format.'
              'We can process JPEG, GIF, PNG, BMP, TIFF, and ICO files.')
        except images.LargeImageError:
          self.error(400)
          self.response.out.write(
              'Sorry, the image provided was too large for us to process.')

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

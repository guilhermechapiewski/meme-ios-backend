#!/usr/bin/env python
import urllib

from google.appengine.ext import blobstore, webapp
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext.webapp.util import run_wsgi_app

class MainHandler(webapp.RequestHandler):
    def get(self):
        upload_url = blobstore.create_upload_url('/img/upload')
        self.response.out.write('''
        <html>
            <head>
                <title>Yahoo! Meme iOS Backend application</title>
            </head>
            <body>
                <form action="%s" method="POST" enctype="multipart/form-data">
                    Upload File: <input type="file" name="file"><br>
                    <input type="submit" name="submit" value="Submit">
                </form>
            </body>
        </html>
        ''' % upload_url)
        

class ImgHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

class ImgUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def post(self):
        upload_files = self.get_uploads('file')
        blob_info = upload_files[0]
        self.redirect('/img/%s' % blob_info.key())

def main():
    application = webapp.WSGIApplication([
                ('/', MainHandler),
                ('/img/([^/]+)?', ImgHandler),
                ('/img/upload', ImgUploadHandler),
            ], 
            debug=True)
    run_wsgi_app(application)

if __name__ == '__main__':
    main()

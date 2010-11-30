import datetime
import hashlib

from django.utils import simplejson 
from google.appengine.ext import db, blobstore, webapp
from google.appengine.ext.webapp import blobstore_handlers

from models import App, Image

class ImageHandler(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, img_key):
        image = None
        try:
            image = db.get(img_key)
        except:
            self.error(404)
            self.response.out.write('Image not found.')
        
        if image:
            self.response.headers['Content-Type'] = str(image.content_type)
            self.send_blob(blobstore.BlobInfo.get(image.blob_key))

class ImageExpirationHandler(webapp.RequestHandler):
    def get(self):
        if self.request.headers.get('X-AppEngine-Cron', 'false') == 'true':
            now = datetime.datetime.now()
            half_hour_ago = now - datetime.timedelta(minutes=30)
            for image in Image.all().filter('date <', half_hour_ago):
                image_blob = blobstore.BlobInfo.get(image.blob_key)
                if image_blob:
                        image_blob.delete()
                image.delete()

class ImageUploadUrlHandler(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps({ 
            'url': blobstore.create_upload_url('/v1/img/upload'),
        }))
    
class ImageUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
    def auth(self):
        '''
        app_name = self.request.headers.get('X-MemeApp-AppId', None)
        img_type = self.request.headers.get('X-MemeApp-Type', None)
        img_size = self.request.headers.get('X-MemeApp-Size', None)
        auth = self.request.headers.get('X-MemeApp-Auth', None)
        
        if not app_name or not img_type or not img_size or not auth:
            self.error(400)
            self.response.out.write('Authentication required')
            return False
        
        app = App.all().filter('name = ', app_name)
        verification = 'type:%s|%s|secret:%s' % (img_type, img_size, app.secret)
        
        if auth != hashlib.md5(verification).hexdigest():
            self.error(403)
            self.response.out.write('Forbidden')
            return False
        '''
        return True
    
    def post(self):
        upload_files = self.get_uploads('file')
        file_info = upload_files[0]
    
        image = Image(
            blob_key=str(file_info.key()), 
            content_type=file_info.content_type, 
            date=datetime.datetime.now()
        )
        image.put()
    
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps({ 
            'id': str(image.key()), 
            'content_type': str(image.content_type), 
            'url': 'http://%s/v1/img/%s' % (self.request.headers['Host'], image.key()),
        }))
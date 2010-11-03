import datetime
import hashlib

from django.utils import simplejson 
from google.appengine.ext import db, webapp

from models import App, Image

class ImageHandler(webapp.RequestHandler):
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

class ImageExpirationHandler(webapp.RequestHandler):
    def get(self):
        if self.request.headers.get('X-AppEngine-Cron', 'false') == 'true':
            now = datetime.datetime.now()
            one_hour_ago = now - datetime.timedelta(hours=1)
            db.delete(Image.all().filter('date <', one_hour_ago))

class ImageUploadHandler(webapp.RequestHandler):
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
        if self.auth():        
            img_data = self.request.POST.get('file').file.read()
            content_type = self.request.POST.get('file').type
        
            image = Image(
                data=img_data, 
                content_type=content_type, 
                date=datetime.datetime.now()
            )
            image.put()
        
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(simplejson.dumps({ 
                'id': str(image.key()), 
                'content_type': str(image.content_type), 
                'url': 'http://%s/img/%s' % (self.request.headers['Host'], image.key()),
            }))
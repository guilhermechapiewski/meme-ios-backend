#!/usr/bin/env python
import datetime

import wsgiref.handlers
from django.utils import simplejson 
from google.appengine.ext import db, webapp

from models import Image

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('''
        <html>
            <head>
                <title>Yahoo! Meme iOS Backend application</title>
                <script type="text/javascript" charset="utf-8" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>
                <script type="text/javascript" charset="utf-8">
                $(document).ready(function() {
                    $('#generate_bookmarklet').click(function(){
                        var js = $('#bookmarklet_js').val();
                        js = js.replace('#username#', $('#meme_username').val());
                        $('#bookmarklet').attr('href', js);
                        $('#bookmarklet_text').show();
                    });
                });
                </script>
            </head>
            <body>
                <h1>Yahoo! Meme iOS Backend application</h1>
                <h2>1) Image upload</h2>
                <p>
                    <form action="/img/upload" method="POST" enctype="multipart/form-data">
                        Upload File: <input type="file" name="file"> <input type="submit" name="submit" value="Submit">
                    </form>
                </p>
                <h2>2) Post later</h2>
                <p>
                    <input type="hidden" id="bookmarklet_js" value="javascript:(function(){window.open('http://%s/postlater/add?username=#username#&url='+encodeURIComponent(location.href));})();">
                    Type your Meme username here: <input type="text" id="meme_username"> <input type="button" id="generate_bookmarklet" value="Generate my bookmarklet!"><br>
                    <span style="display:none;" id="bookmarklet_text">Drag this link to your bookmarks bar: <b><a id="bookmarklet" href="#">Post later to Meme</a></b></span>
                </p>
            </body>
        </html>
        ''' % self.request.headers['Host'])

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
        if self.request.headers['X-AppEngine-Cron'] == 'true':
            now = datetime.datetime.now()
            one_hour_ago = now - datetime.timedelta(hours=1)
            db.delete(Image.all().filter('date <', one_hour_ago))

class ImageUploadHandler(webapp.RequestHandler):
    def post(self):
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

def main():
    application = webapp.WSGIApplication([
                ('/', MainHandler),
                ('/img/expiration', ImageExpirationHandler),
                ('/img/upload', ImageUploadHandler),
                ('/img/(.+)', ImageHandler),
            ], 
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()

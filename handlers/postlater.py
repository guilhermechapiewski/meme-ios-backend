import datetime

from django.utils import simplejson
from google.appengine.ext import db, webapp

from models import Post

class PostLaterAddHandler(webapp.RequestHandler):
    def get(self):
        post = Post(
            username=self.request.get('username'), 
            url=self.request.get('url'), 
            date=datetime.datetime.now()
        )
        post.put()
        
        self.response.out.write('''
        <html>
            <head>
                <title>Yahoo! Meme iOS Backend application</title>
            </head>
            <body>
                <script type="text/javascript" charset="utf-8">
                    window.close();
                </script>
            </body>
        </html>
        ''')
        
class PostLaterHandler(webapp.RequestHandler):
    def get(self, username):
        posts = Post.all().filter('username =', username).order('date')

        posts_data = []
        for post in posts:
            posts_data.append({
                'id': str(post.key()), 
                'url': post.url, 
                'date': post.date.isoformat(), 
            })

        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(simplejson.dumps(posts_data))
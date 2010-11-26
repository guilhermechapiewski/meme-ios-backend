import os

from google.appengine.api import users
from google.appengine.ext import blobstore, webapp
from google.appengine.ext.webapp import template

from models import Highlight

class AdminHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if users.get_current_user():
            if users.is_current_user_admin():
                highlight_id = 'meme_ipad_dashboard'
                highlight_query = None
                highlight_amount = None
                highlights = Highlight.all().filter('name =', highlight_id)

                for highlight in highlights:
                    highlight_query = highlight.query
                    highlight_amount = highlight.amount
                
                template_values = { 
                    'img_upload_url': blobstore.create_upload_url('/v1/img/upload'), 
                    'host': self.request.headers['Host'],
                    'logout_url': users.create_logout_url('/'),
                    'highlight_id': highlight_id,
                    'highlight_query': highlight_query,
                    'highlight_amount': highlight_amount,
                }
                path = os.path.join(os.path.dirname(__file__), '../templates/admin.html')
                self.response.out.write(template.render(path, template_values))
            else:
                self.error(403)
                self.response.out.write('<html><body><h1>Forbidden</h1><a href=\"%s\">sign out</a></body></html>' % users.create_logout_url('/'))
        else:
            self.response.out.write('<html><body><a href=\"%s\">sign in</a></body></html>' % users.create_login_url('/admin'))
            
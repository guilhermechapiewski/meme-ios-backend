import os

from google.appengine.api import users
from google.appengine.ext import blobstore, webapp
from google.appengine.ext.webapp import template

class AdminHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        if users.get_current_user():
            if users.is_current_user_admin():
                template_values = { 
                    'img_upload_url': blobstore.create_upload_url('/img/upload'), 
                    'host': self.request.headers['Host'],
                    'logout_url': users.create_logout_url('/'),
                    'highlight_query': 'poker',
                    'highlight_amount': '1',
                }
                path = os.path.join(os.path.dirname(__file__), '../templates/admin.html')
                self.response.out.write(template.render(path, template_values))
            else:
                self.error(403)
                self.response.out.write('<html><body><h1>Forbidden</h1><a href=\"%s\">sign out</a></body></html>' % users.create_logout_url('/'))
        else:
            self.response.out.write('<html><body><a href=\"%s\">sign in</a></body></html>' % users.create_login_url('/admin'))
            
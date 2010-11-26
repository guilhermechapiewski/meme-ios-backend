import datetime

from django.utils import simplejson
from google.appengine.ext import db, webapp

from models import Highlight

class HighlightUpdateHandler(webapp.RequestHandler):
    def post(self):
        highlight = Highlight(
            name=self.request.get('highlight_name'), 
            query=self.request.get('highlight_query'), 
            amount=int(self.request.get('highlight_amount')), 
        )
        highlight.put()
        
        self.redirect('/admin')
        
class HighlightHandler(webapp.RequestHandler):
    def get(self, name):
        highlights = Highlight.all().filter('name =', name)
        highlight_data = None
        
        for highlight in highlights:
            highlight_data = {
                'name': highlight.name, 
                'query': highlight.query, 
                'amount': highlight.amount, 
            }
        
        if highlight_data:
            self.response.headers['Content-Type'] = 'application/json'
            self.response.out.write(simplejson.dumps(highlight_data))
        else:
            self.error(404)
            self.response.out.write('Not found')
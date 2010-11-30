import datetime

from django.utils import simplejson
from google.appengine.ext import db, webapp

from models import Highlight

class HighlightUpdateHandler(webapp.RequestHandler):
    def post(self):
        highlights = Highlight.all().filter('name =', self.request.get('highlight_name'))
        highlight = None
        
        # try to find the highlight already persisted
        for h in highlights:
            highlight = h
        
        # if highlight wasn't found, means that we sould create another one
        if highlight is None:
            highlight = Highlight(name=self.request.get('highlight_name'))
        
        # add new data to highlight and...
        highlight.query = self.request.get('highlight_query')
        highlight.amount = int(self.request.get('highlight_amount'))
        
        # ...create or update
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
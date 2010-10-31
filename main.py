import wsgiref.handlers
from google.appengine.ext import webapp

class MainHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('Meme iOS Backend appliction')

class UploadHandler(webapp.RequestHandler):
    def get(self):
        self.response.out.write('TO DO')

def main():
    application = webapp.WSGIApplication([
                    ('/', MainHandler),
                    ('/upload/.*', UploadHandler),
            ], 
            debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == '__main__':
    main()

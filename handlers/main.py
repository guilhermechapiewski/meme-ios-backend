from google.appengine.ext import blobstore, webapp

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
                    <form action="%s" method="POST" enctype="multipart/form-data">
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
        ''' % (
            blobstore.create_upload_url('/img/upload'), 
            self.request.headers['Host'],
        ))
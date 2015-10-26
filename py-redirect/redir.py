import SimpleHTTPServer
import SocketServer

class myHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        print self.path
        self.send_response(301)
        new_path = '%s%s'%('https://docs.google.com/forms/d/1rMNJQoVcvzK9gUM1gEHOmCcRNKVfxrVgMz6coNj5NY4/viewform?usp=send_form', self.path)
        self.send_header('Location', new_path)
        self.end_headers()

PORT = 80
handler = SocketServer.TCPServer(("", PORT), myHandler)
print "serving at port " + str(PORT)
handler.serve_forever()

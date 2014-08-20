import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.options
import json
import pprint
import realtime as rt
import history as his

client = list() 

class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("index.html", messages=None)

class realtimeHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("realtime.html")    
 
    def post(self):
            # new dictionary
        response_to_send = {}
                 
       
        response_to_send['c']=rt.realTimeData('CTSVRMS01')
       
        print('Response to return')
        pprint.pprint(response_to_send)
    
        self.write(json.dumps(response_to_send)) 
class historyHandler(tornado.web.RequestHandler):
    
    def get(self):
        self.render("history.html")    
 
    def post(self):
            # new dictionary
        response_to_send = {}
                 
        response_to_send=his.historydata()
        
       
        print('Response to return')
        pprint.pprint(response_to_send)
    
        self.write(json.dumps(response_to_send))          

class realtimeWSHandler(tornado.websocket.WebSocketHandler):

    def open(self):
        client.append(self)
      
    def on_close(self):
        client.remove(self)
  
    def on_message(self, message):
        response_to_send = {}
                 
        
        response_to_send['c']=rt.realTimeData()
       
        print('Response to return')
        pprint.pprint(response_to_send)
    
        self.write(json.dumps(response_to_send))
  
            
class aboutHandler(tornado.web.RequestHandler):

    def get(self):
        self.render("about.html")    

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/realtime/", realtimeHandler),
            (r"/realtime/ws", realtimeWSHandler),
            (r"/history/", historyHandler),
            (r"/about/", aboutHandler)
        ]
        
        settings = {
            'template_path': 'templates',
            'static_path': 'static'
        }
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == '__main__':
    
    tornado.options.parse_command_line()
    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()

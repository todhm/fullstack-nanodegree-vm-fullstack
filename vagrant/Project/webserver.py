from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, Base, MenuItem
import re
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            #define hello
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                print self.path
                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'>"
                output += "<h2>What would you like me to say?</h2><input name = 'message' type = 'text'>"
                output += "<input type = 'submit' value = 'Submit'></form>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return

            #define restaurant
            elif self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()


                restaurants = session.query(Restaurant).all()
                output = ""
                output += "<html><body>"
                output += "<a href='/restaurant/new'> Make a New Restaurant</a></br>"
                for row in restaurants:
                    output += "{} </br>".format(row.name)
                    output += "<a href='/restaurant/{}/edit'>Edit </a></br>".format(row.id)
                    output += "<a href='/restaurant/{}/delete'>Delete</a></br>".format(row.id)
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            elif re.search("/restaurant/\d+/edit",self.path):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                restaurant_id = re.search("/restaurant/(\d+)/edit",self.path).group(1)
                restaurant_id = int(restaurant_id)
                restaurant_name = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
                output = ""
                output += "<html><body>"
                output += "<h2>{}</h2>".format(restaurant_name.name)
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurant/{}/edit'>".format(restaurant_id)
                output += "<input name = 'edit_menu' type = 'text' placeholder = '{}'>".format(restaurant_name.name)
                output += "<input type = 'submit' value = 'Edit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                return

            elif self.path.endswith('/delete'):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                restaurant_id = self.path.split('/')[2]
                restaurant_id = int(restaurant_id)
                restaurant_name = session.query(Restaurant).filter(Restaurant.id == restaurant_id).one()
                output = ""
                output += "<html><body>"
                output += "<h2>Are you sure you want to delete {}</h2>".format(restaurant_name.name)
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurant/{}/delete'>".format(restaurant_id)
                output += "<input type = 'submit' value = 'Delete'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                return

            elif self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h2> Make a New Restaurant </h2>"
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/restaurant/new'>"
                output += "<input name = 'add_menu' type = 'text' placeholder = 'New Restaurant name'>"
                output += "<input type = 'submit' value = 'Create'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                return


            elif self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "&#161Hola!"
                output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'>"
                output += "<h2>What would you like me to say?</h2><input name = 'message' type = 'text'>"
                output += "<input type = 'submit' value = 'Submit'></form>"
                output += "</body></html>"

                self.wfile.write(output)
                print output
                return

        except Exception as e:

            self.send_error(404,"File not Found %s" % self.path)
            session.close()


    def do_POST(self):
        try:
            if self.path.endswith("/restaurant/new") :
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                restaurant_name = fields.get('add_menu')
                restaurant_name = str(restaurant_name[0])
                new_restaurant = Restaurant(name=restaurant_name)
                session.add(new_restaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurant')
                self.end_headers()
                return
            if re.search("/restaurant/\d+/edit",self.path):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                edited_name = fields.get('edit_menu')[0]
                restaurant_id = re.search("/restaurant/(\d+)/edit",self.path).group(1)
                restaurant_id = int(restaurant_id)
                session.query(Restaurant)\
                       .filter(Restaurant.id == restaurant_id)\
                       .update({'name':edited_name})
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurant')
                self.end_headers()
                return

            if self.path.endswith('/delete'):
                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                delete_id = self.path.split('/')[2]
                session.query(Restaurant)\
                        .filter(Restaurant.id == delete_id)\
                        .delete()
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location','/restaurant')
                self.end_headers()
                return

            #if self.patn.endswith("/restaurant/<string:restaurant_id>/edit")

            '''
            self.send_response(301)
            self.end_headers()


            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')
                restaurant_name = fields.get('add_menu')

            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s </h1>" %messagecontent[0]

            output += "<form method = 'POST' enctype = 'multipart/form-data' action = '/hello'>"
            output += "<h2>What would you like me to say?</h2><input name = 'message' type = 'text'>"
            output += "<input type = 'submit' value = 'Submit'></form>"
            output += "</body></html>"
            self.wfile.write(output)
            print output
            '''


                #return
        except Exception as e:
            print e
            session.close()
            pass




def main():
    try:
        port = 8080
        server = HTTPServer(('',port),webserverHandler)
        print "webserver running on port %s" %port
        server.serve_forever()
    except KeyboardInterrupt:
        print "^C entered, stopping webserver"
        server.socket.close()


if __name__ == '__main__':
    main()

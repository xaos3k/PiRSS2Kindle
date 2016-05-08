import os
import sys
import sqlite3
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado import autoreload
from tornado.options import define, options

define("port", default=8000, help="")
DBName = 'PiRSS2Kindle.sqlite'

class IndexHandler(tornado.web.RequestHandler):
    con = sqlite3.connect(DBName)
    def get(self):
        con = sqlite3.connect(DBName)
        with con:
            kindlemail = ""
            RSSlist = []
            try:
                cur = con.cursor()
                cur.execute("CREATE TABLE KindleRSS(Id INTEGER PRIMARY KEY, Address TEXT)")
                cur.execute("CREATE TABLE KindleMail(Id INT, Address TEXT)")
                DBKindleMail = 'INSERT INTO KindleMail VALUES(1, \'add@mail.here\')'
                cur.execute(DBKindleMail)
                cur.execute("SELECT * FROM KindleMail")
                row = cur.fetchone()
                kindlemail = row[1]
            except sqlite3.Error, e:
                cur.execute("SELECT * FROM KindleMail")
                row = cur.fetchone()
                kindlemail = row[1]

                cur.execute("SELECT * FROM KindleRSS")
                RSSlist = []
                while True:
                    row = cur.fetchone()
                    if row == None:
                        break
                    entry = row[1]
                    RSSlist.append(entry)
                    print row[0], row[1]
        self.render('index.html', kindlemail=kindlemail, RSSlist=RSSlist)

    def post(self):
        kindlemail = ""
        RSSlist = []
        if self.get_argument("rssb", None) != None:
            feed = self.request.arguments['rss']
            con = sqlite3.connect(DBName)
            with con:
                cur = con.cursor()
                DBKindleRSS = 'INSERT INTO KindleRSS VALUES(NULL, \'' + feed[0] +'\')'
                cur.execute(DBKindleRSS)
            print feed

        if self.get_argument("kindlemailb", None) != None:
            kindlemail = self.request.arguments['kindlemail']
            print kindlemail
            con = sqlite3.connect(DBName)
            with con:
                cur = con.cursor()
                DBKindleMail = 'UPDATE KindleMail SET Address = \'' + kindlemail[0] +'\' WHERE ID = 1'
                cur.execute(DBKindleMail)

        self.render('index.html', kindlemail=kindlemail, RSSlist=RSSlist)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/(.*)', tornado.web.StaticFileHandler, {'path': 'templates'}),
            (r'/css/(.*)', tornado.web.StaticFileHandler, {'path': 'css'})
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        debug=True,
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    ioloop = tornado.ioloop.IOLoop().instance()
    autoreload.start(ioloop)
    ioloop.start()

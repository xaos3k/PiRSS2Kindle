import os
import sys
import sqlite3
import feedparser
import time

kindlemail = "insert@yourkindlemail.here"
today = time.strftime("%d-%m-%Y--%H-%M-%S")
print "creating file: " + today + ".html"
filename = today + ".html"

def create():
    print "getting news..."
    file = open(filename,'a')
    file.write("<html><head><meta http-equiv=\"content-type\" content=\"text/html; charset=UTF-8\"><title>Test</title></head><body>")
    DBName = 'PiRSS2Kindle.sqlite'
    con = sqlite3.connect(DBName)
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM KindleRSS")
        RSSlist = []
        title = ""
        while True:
            row = cur.fetchone()
            if row == None:
                break
            entry = row[1]
            d = feedparser.parse(entry)
            title = d['feed']['title']
            unread = len(d['entries'])
            file.write("<a href=\"#" + title + "\">" + title + "</a> (" + str(unread) + ")<br />")
        file.write("<mbp:pagebreak />")

        cur = con.cursor()
        cur.execute("SELECT * FROM KindleRSS")
        while True:
            row = cur.fetchone()
            if row == None:
                break
            entry = row[1]
            RSSlist.append(entry)
            d = feedparser.parse(entry)
            title = d['feed']['title']
            print title
            print row[0], row[1]
            file.write("<div id=\"" + title + "\">" + title + "<mbp:pagebreak />")
            for post in d.entries:
                file.write("<b>" + post.title.encode("utf-8") + "</b><br />" + post.summary.encode("utf-8") + "<br /><br />")
            file.write("</div><mbp:pagebreak />")
    print "writing news to file..."
    file.write("</body></html>")
    file.close()
create()



try:
    print "sending file..."
    os.system("echo \"\" | mail -s \"convert\" -A " + filename + " " + kindlemail)
except:
    print "nope"

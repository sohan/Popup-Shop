import sys
sys.stdout = sys.stderr

import atexit
import threading
import cherrypy
import smtplib
import string

cherrypy.config.update({'environment': 'embedded'})

if cherrypy.__version__.startswith('3.0') and cherrypy.engine.state == 0:
    cherrypy.engine.start(blocking=False)
    atexit.register(cherrypy.engine.stop)

class Root(object):
    def index(self):
        return 'Hello World!'
    index.exposed = True

def add_to_mailing_list(email):
    SUBJECT = "join"
    TO = "sj346@cornell.edu"
    FROM = email
    text = ""
    BODY = string.join((
            "From: %s" % FROM,
            "To: %s" % TO,
            "Subject: %s" % SUBJECT ,
            "",
            text
            ), "\r\n")
    server = smtplib.SMTP('localhost')
    server.sendmail(FROM, [TO], BODY)
    server.quit()

#application = cherrypy.Application(Root(), script_name=None, config=None)
if __name__ == '__main__':
    add_to_mailing_list('sj346@cornell.edu')

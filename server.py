import sys
sys.stdout = sys.stderr

import os
import cherrypy
import smtplib
import string
from cherrypy import tools
import re

class Root(object):
    def __init__(self):
        self.server = smtplib.SMTP('localhost')

    @cherrypy.expose
    def index(self):
        return 'Sup, world?'

    @cherrypy.expose
    @tools.json_out(on = True)
    def add_to_mailing_list(self, email = None):
        if not email:
            return {'error': 'no email address entered.'}
        if not re.match(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$", email):
            return {'error': 'invalid email address enetered.'}
        try:
            SUBJECT = "join"
            TO = "popshop-request-l@cornell.edu"
            FROM = email
            text = ""
            BODY = string.join((
                    "From: %s" % FROM,
                    "To: %s" % TO,
                    "Subject: %s" % SUBJECT ,
                    "",
                    text
                    ), "\r\n")
            self.server.sendmail(FROM, [TO], BODY)
            return {'success': True}
        except Exception, e:
            return {'success': False, 'error': str(e)}

current_dir = os.path.dirname(os.path.abspath(__file__))
config_file = os.path.join(current_dir, 'server_config.ini')
cherrypy.config.update(config_file)
cherrypy.tree.mount(Root(), '/api')

if __name__ == '__main__':
    cherrypy.engine.start()

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import json

import cgi


class FormPage(Resource):
    def render_GET(self, request):
        #return '<html><body><form method="POST"><input name="the-field" type="text" /></form></body></html>'
        return '<html><body>GET action not allowed</body></html>'

    def render_POST(self, request):
        self.parse_post(cgi.escape(request.args["the-field"][0]))
        return "Thanks!"

    def parse_post(self, input):
        data = json.loads(input)

    #    print "Issue Info: {0}\n\n".format(data['issue'])
    #    print "Issue Info: {0}\n\n".format(data['issue']['title'])
    #    print "Issue URL: {0}\n\n".format(data['issue']['html_url'])
    #    print "Action Info: {0}\n\n".format(data['action'])
    
    #   Format issues as below
    #   Issue CLOSED - saltstack/salt: #1888 (Add daemonize_if to service.restart for the minion) <https://github.com/saltstack/salt/issues/1888>

        issue_str = 'Issue {0} - {1}: #{2} ({3}) ' \
        '<{4}>'.format(data['action'].upper(), data['repository']['full_name'], 
        data['issue']['number'], data['issue']['title'],  data['issue']['html_url'])
    
        print issue_str

class IssueServer():

    def __init__(self, port=8880, paths=[]):


        root = Resource()
        root.putChild("form", FormPage())
        factory = Site(root)
        reactor.listenTCP(8880, factory)
        reactor.run()

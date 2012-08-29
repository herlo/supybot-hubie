###
# Copyright (c) 2012, Clint Savage
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import supybot.utils as utils
import supybot.ircmsgs as ircmsgs
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor
import json

import cgi


class PostPage(Resource):

    def __init__(self, irc):
        self.irc = irc

    def render_GET(self, request):
        return '<html><body><form method="POST"><input name="data" type="text" /></form></body></html>'
        #return '<html><body>GET action not allowed</body></html>'

    def render_POST(self, request):
        self.parse_post(cgi.escape(request.args["data"][0]))
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
    
        for channel in self.irc.state.channels:
            self.irc.queueMsg(ircmsgs.privmsg(channel, issue_str))

        print issue_str


class Hubie(callbacks.Plugin):
    """Add the help for "@plugin help Hubie" here
    This should describe *how* to use this plugin."""
    threaded = True

    def __init__(self, irc):

        '''
        Initialize the twisted web server with the proper 
        ports and URI values.
        '''

        callbacks.Plugin.__init__(self, irc)


        if not reactor:
            self.irc.error('Twisted is not installed.')

        # ensure we have the irc object in self
        self.irc = irc

        root = Resource()
        for uri in self.registryValue('uris'):
            root.putChild(uri, PostPage(irc))

        factory = Site(root)
        reactor.listenTCP(self.registryValue('port'), factory)

#       because this is supybot and it already has twisted going
#       we don't run the reactor

#        reactor.run()

Class = Hubie


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

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

import supybot.conf as conf
import supybot.registry as registry

def configure(advanced):
    # This will be called by supybot to configure this module.  advanced is
    # a bool that specifies whether the user identified himself as an advanced
    # user or not.  You should effect your configuration by manipulating the
    # registry as appropriate.
    from supybot.questions import expect, anything, something, yn
    conf.registerPlugin('Hubie', True)

Hubie = conf.registerPlugin('Hubie')
# This is where your configuration variables (if any) should go.  For example:
# conf.registerGlobalValue(Hubie, 'someConfigVariableName',
#     registry.Boolean(False, """Help for someConfigVariableName."""))

conf.registerChannelValue(Hubie, 'port', registry.Integer(8880, """The port on which Hubie runs."""))

# it is probably a good idea to really obfuscate your urls. Though it is also
# probably a good idea to use iptables or some firewall tools to limit access
# to the server on which you run this application. 

# The pathmaps value below is a paired entry represented by the first entry, 
# the uri or 'path' which will be appended to your host. The second entry will
# be the channel to which the messages will be sent. In the example below, if
# you posted json data to http://yourhost:8880/saltstack, whatever json you
# posted would be parsed and the resulting message would be displayed in the
# #salt-devel channel (assuming your bot was configured to connect to that
# channel).

conf.registerChannelValue(Hubie, 'pathmaps', registry.CommaSeparatedListOfStrings( ['saltstack', '#salt-devel', 'saltstack', '#herlo'], """List of allowed path references to use in the web server. Ensure the channels line up with these paths or you will get messages in the wrong channels."""))
conf.registerChannelValue(Hubie, 'description', registry.String("I am Hubie, the github issues and events bot!. More information is available at http://github.com/herlo/supybot-hubie/", """Description of this plugin"""))

# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:

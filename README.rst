githubie
========

githubie (pronounced git hew bee) is a plugin that provides updates
and allows queries to the github issue interface using events. While
hubot (https://github.com/github/hubot) is nice, it's a bit overkill
for managing just issues and statuses.

It is possible githubie will grow to a much greater state and allow
more interaction to registered users and allow gists and more. For now,
however, githubie just focuses on issues and event notifications from
github.

Dependencies
------------

The following dependencies are required (though it appears they are part
of the core python stdlib).

- json
- cgi

Configuration
-------------

To configure supybot-hubie is a bit tricky. First off, one must know that
SSL is required since we're taking advantage of the fact that supybot uses
twisted. SSL is the only way to connect to an irc server with supybot's
twisted functionality.

When configuring this, I discovered some workarounds that will help you
get supybot-hubie up and running.

#. After performing the supybot-wizard and adding the 'Hubie' plugin,
   edit the configuration file. In this configuration file, make sure the
   following values are changed as appropriate:

   supybot.networks.freenode.ssl: True

   supybot.networks.freenode.servers: chat.us.freenode.net:7000

   It is important to note that the server and its port should be set
   as shown above. If it is set differently, the SSL connection may not
   work. Also, it has been discovered that occasionally, the above server
   will return an IPV6 address which twisted does not yet work with inside
   supybot.

#. Make sure to include any channels which should receive messages. This is
   done by editing the same configuration file like so:

   supybot.networks.freenode.channels: #herlo #salt-devel

#. The pathmaps need to be setup. The easiest way to do this is to
   again modify the same configuration file to look like so:

   supybot.plugins.Hubie.pathmaps: saltstack, #salt-devel, gooseproject, #herlo

   These pathmaps are configured in pairs. The first is the http path to visit
   when performing a callback POST action from github. The second of the pair
   is the channel in which the http path will send its message.  For example, 
   if the first pair above were used, the url might look like so:

   http://yourhost:8880/saltstack

#. Once all setup, it can be tested by sending the appropriate json message to the
   URL. To test it, one can just open a browser and point to http://yourserver:8880/path
   where a form will be presented. Fill in proper json as represented by the events
   api in github and the message should appear properly in the appropriate channel.



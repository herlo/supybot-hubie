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

The following dependencies are required::

- Twisted Web (yum install python-twisted-web)
- Twisted Names (yum install python-twisted-names)

Configuration
-------------

There are two parts to configuring supybot-hubie. The first is to setup a
hook on the github site. This is not a standard hook, but a pubsubhubbub
hook. The github documentation is a good resource to get started,
http://developer.github.com/v3/repos/hooks/#pubsubhubbub for reference.

To enable an event hook which supyboty-hubie will use, it must be in the 
following form::

  curl -i -u "<user>" https://api.github.com/hub -Fhub.mode=subscribe \
  -Fhub.topic=https://github.com/<user>/<repo>/events/issues \
  -Fhub.callback=http://<fqdn>:8880/<pathmap>

Using the configurations from below, it might look something like::

  curl -i -u "herlo" https://api.github.com/hub -Fhub.mode=subscribe \
  -Fhub.topic=https://github.com/herlo/supybot-hubie/events/issues \
  -Fhub.callback=http://my.hostname.org:8880/supybot-hubie

Enter the github password for the user. Output should look something like::

  HTTP/1.1 100 Continue
  
  HTTP/1.1 204 No Content
  Server: GitHub.com
  Date: Sat, 26 Jan 2013 22:41:49 GMT
  Connection: keep-alive
  Status: 204 No Content
  X-RateLimit-Remaining: 4996
  Cache-Control:
  X-Content-Type-Options: nosniff
  X-GitHub-Media-Type: github.beta
  X-RateLimit-Limit: 5000

Verify the hook now exists on the repository. This is done under 'Settings'
> 'Service Hooks' > 'WebHook URLs'. If the callback url doesn't exist, perform
the command above again.

..note: Adding the hook to the 'WebHook URLs' directly will NOT work.

To configure supybot-hubie is a bit tricky. First off, one must know that
SSL is required since we're taking advantage of the fact that supybot uses
twisted. SSL is the only way to connect to an irc server with supybot's
twisted functionality.

When configuring this, I discovered some workarounds that will help you
get supybot-hubie up and running.

#. After performing the supybot-wizard and adding the 'Hubie' plugin,
   edit the configuration file. In this configuration file, make sure the
   following values are changed as appropriate:

   supybot.drivers.module: Twisted

   supybot.networks.freenode.ssl: True

   supybot.networks.freenode.servers: niven.freenode.net:7070

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

   supybot.plugins.Hubie.pathmaps: saltstack, #salt-devel, supybot-hubie, #herlo

   These pathmaps are configured in pairs. The first is the http path to visit
   when performing a callback POST action from github. The second of the pair
   is the channel in which the http path will send its message.  For example, 
   if the first pair above were used, the url might look like so:

   http://yourhost:8880/saltstack

#. Once all setup, it can be tested by sending the appropriate json message to the
   URL. To test it, one can just open a browser and point to http://yourserver:8880/path
   where a form will be presented. Fill in proper json as represented by the events
   api in github and the message should appear properly in the appropriate channel.



#!/usr/bin/env python
# coding: utf-8

# Copyright (C) 2010 Arthur Furlan <afurlan@afurlan.org>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# On Debian systems, you can find the full text of the license in
# /usr/share/common-licenses/GPL-3

# Extended by larsfp@cl.no 20110422.
# TODO: Logging for statistics, and anti-cheating

from jabberbot import JabberBot, botcmd
from datetime import datetime
import re
import urllib

#from lunch.py import Lunchpicker:
import lunch

class MUCJabberBot(JabberBot):

    ''' Add features in JabberBot to allow it to handle specific
    caractheristics of multiple users chatroom (MUC). '''

    def __init__(self, *args, **kwargs):
        ''' Initialize variables. '''

        # answer only direct messages or not?
        self.only_direct = kwargs.get('only_direct', False)
        try:
            del kwargs['only_direct']
        except KeyError:
            pass

        # initialize jabberbot
        super(MUCJabberBot, self).__init__(*args, **kwargs)

        # create a regex to check if a message is a direct message
        user, domain = str(self.jid).split('@')
        self.direct_message_re = re.compile('^%s(@%s)?[^\w]? ' \
                % (user, domain))

    def callback_message(self, conn, mess):
        ''' Changes the behaviour of the JabberBot in order to allow
        it to answer direct messages. This is used often when it is
        connected in MUCs (multiple users chatroom). '''

        message = mess.getBody()
        if not message:
            return

        if self.direct_message_re.match(message):
            mess.setBody(' '.join(message.split(' ', 1)[1:]))
            return super(MUCJabberBot, self).callback_message(conn, mess)
        elif not self.only_direct:
            return super(MUCJabberBot, self).callback_message(conn, mess)


class LunchBot(MUCJabberBot):

    @botcmd
    def help(self, mess, args):
        reply = "Commands: gettime, employeeoftheday, coffeeleft"
        self.send_simple_reply(mess, reply)

    @botcmd
    def gettime(self, mess, args):
        now = datetime.now()
        print mess
        #hack for mx date
        mx = str(mess).find("mx")
        if mx > 0:
            print "MX: ", now + datetime.timedelta(hours=-6)
        reply = now.strftime('%Y-%m-%d %h:%M:%s')
        self.send_simple_reply(mess, reply)

    @botcmd
    def lunchlottery(self, mess, args):
        reply = "No, no! You've got it all wrong. I'm not a lunch-bot. Try help."
        self.send_simple_reply(mess, reply)

    @botcmd
    def employeeoftheday(self, mess, args):
        picker = lunch.Lunchpicker()
        luckyfella = picker.pick()
        reply = "%s selected for employee of the day. If (s)he's not here, ask again!" \
            % luckyfella
        self.status_message = "%s picked for %s by %s" % \
            (luckyfella,
            str(datetime.now().strftime('%Y-%m-%d')),
            mess.getFrom())
        self.send_simple_reply(mess, reply)

    @botcmd
    def coffeeleft(self, mess, args):
        f = urllib.urlopen("http://graph.no/?simple=1")
        s = f.read()
        f.close()
        reply = "Coffee at %s: %s grams" % \
            (str(datetime.now().strftime('%Y-%m-%d')),
            str(s))
        self.send_simple_reply(mess, reply)

if __name__ == '__main__':

    username = 'bot@example.com'
    password = 'password'
    nickname = 'Bot'
    chatroom = 'roomname@conference.example.com'

    mucbot = LunchBot(username, password, only_direct=False)
    mucbot.join_room(chatroom)
    mucbot.serve_forever()

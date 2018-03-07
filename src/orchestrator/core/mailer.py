#
# Copyright 2018 Telefonica Espana
#
# This file is part of IoT orchestrator
#
# IoT orchestrator is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# IoT orchestrator is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with IoT orchestrator. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot_support at tid dot es
#
# Author: IoT team
#
import json
import logging
import smtplib

from orchestrator.common.util import RestOperations

logger = logging.getLogger('orchestrator_core')


class MailerOperations(object):

    def __init__(self,
                 MAILER_HOST=None,
                 MAILER_PORT=None,
                 MAILER_USER=None,
                 MAILER_PASSWORD=None,
                 MAILER_FROM=None,
                 MAILER_TO=None,
                 CORRELATOR_ID=None,
                 TRANSACTION_ID=None):

        self.smtp_server = MAILER_HOST
        self.smtp_port = MAILER_PORT
        self.smtp_user = MAILER_USER
        self.smtp_password = MAILER_PASSWORD
        self.smtp_from = MAILER_FROM
        self.smtp_to = MAILER_TO

    def checkMailer(self):
        # TBD
        None


    def sendMail(self, to=None, subject=None, text=None):
        if not to:
            to = self.smtp_to

        dest = [to] # must be a list

        #
        # Prepare actual message
        #
        mail_headers = ("From: \"%s\" <%s>\r\nTo: %s\r\n"
                        % (self.smtp_from,
                           self.smtp_from,
                           ", ".join(dest)))

        msg = mail_headers
        msg += ("Subject: %s\r\n\r\n" % subject)
        msg += text

        #
        # Send the mail
        #
        try:
            # TODO: server must be initialized by current object
            server = smtplib.SMTP(self.smtp_server,
                                  self.smtp_port)
        except smtplib.socket.gaierror:
            logger.error('SMTP socket error')
            return { "error": "SMTP socket error" }

        server.ehlo()
        server.starttls()
        server.ehlo

        try:
            server.login(self.smtp_user,
                         self.smtp_password)
        except smtplib.SMTPAuthenticationError:
            logger.error('SMTP authentication error')
            return { "error": "SMTP authentication error" }

        try:
            server.sendmail(self.smtp_from, dest, msg)
        except Exception:  # try to avoid catching Exception unless you have too
            logger.error('SMTP autentication error')
            return { "error": "SMTP authentication error" }
        finally:
            server.quit()
        logger.info('email was sent')
        return { "details": "email was sent" }

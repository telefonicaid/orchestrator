import json
import logging
import smtplib

from orchestrator.common.util import RestOperations

logger = logging.getLogger('orchestrator_core')


class MailerOperations(object):

    def __init__(self,
                 MAILER_PROTOCOL=None,
                 MAILER_HOST=None,
                 MAILER_PORT=None,
                 CORRELATOR_ID=None,
                 TRANSACTION_ID=None):
        self.MAILER_PROTOCOL = MAILER_PROTOCOL
        self.MAILER_HOST = MAILER_HOST
        self.MAILER_PORT = int(MAILER_PORT)

        # TODO: read from config
        self.smtp_from
        self.smtp_server
        self.smtp_port
        self.smtp_user
        self.smtp_password
        

    def checkMailer(self):
        #conn = ldap.open(self.LDAP_HOST, self.LDAP_PORT)
        assert conn != None
    

    def send_email(self, to, subject, text):

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
            return False

        server.ehlo()
        server.starttls()
        server.ehlo

        try:
            server.login(self.smtp_user,
                         self.smtp_password)
        except smtplib.SMTPAuthenticationError:
            logger.error('SMTP authentication error')
            return False

        try:
            server.sendmail(self.smtp_from, dest, msg)
        except Exception:  # try to avoid catching Exception unless you have too
            logger.error('SMTP autentication error')
            return False
        finally:
            server.quit()
        logger.info('email was sent')            
        return True

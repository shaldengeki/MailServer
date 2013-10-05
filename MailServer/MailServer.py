import time
import socket
import imaplib
import smtplib

class MailServer(object):
  def __init__(self, smtp_host, smtp_port, imap_host, username, password):
    self.smtp_host = unicode(smtp_host)
    self.imap_host = unicode(imap_host)
    self.smtp_port = int(smtp_port)
    self.username = unicode(username)
    self.password = unicode(password)
    self.imap = self.imapLogin(self.username, self.password)
    self.smtp = self.smtpLogin(self.username, self.password)
    self.lastSentTime = 0
  def imapLogin(self, username, password):
    imap = imaplib.IMAP4_SSL(self.imap_host)
    imap.login(username, password)
    return imap
  def smtpLogin(self, username, password):
    '''
    Logs into host's SMTP server using the given credentials.
    If this fails, return False. Otherwise, return the SMTP object.
    '''
    smtp = smtplib.SMTP(self.smtp_host, self.smtp_port)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtpLoginResult = smtp.login(username, password)
    if 'Accepted' not in smtpLoginResult[1]:
      return False
    else:
      return smtp
  def send(self, toEmail, ccEmail=[], subject="", body=""):
    '''
    Sends an email and returns the (active) SMTP connection used to do so.
    If email fails to send or failure to log in to SMTP, returns False.
    '''
    # if subject and body are both blank then refuse to send this message.
    if not subject and not body:
      return False
    # rate-limit our emails to once every minute.
    if time.time() < self.lastSentTime + 60:
      return False
    self.lastSentTime = time.time()
      
    # if SMTP server is not set, log in.
    if not self.smtp:
      self.smtp = self.smtpLogin(self.username, self.password)
      if not self.smtp:
        return False
    message = "From: %s\r\n" % self.username + "To: %s\r\n" % toEmail + "CC: %s\r\n" % ",".join(ccEmail) + "Subject: %s\r\n" % subject + "\r\n" + body
    returnDict = False
    for x in range(10):
      try:
        returnDict = self.smtp.sendmail(self.username, [toEmail]+ccEmail, message)
      except (socket.sslerror, smtplib.SMTPServerDisconnected, smtplib.SMTPConnectError):
        # if connection has timed out, log back in and attempt sending this email again.
        self.smtp = self.smtpLogin(self.username, self.password)
        if not self.smtp:
          continue
      except (smtplib.SMTPRecipientsRefused, smtplib.SMTPHeloError, smtplib.SMTPSenderRefused, smtplib.SMTPDataError):
        return False
      except:
        continue
      else:
        break
    return returnDict
